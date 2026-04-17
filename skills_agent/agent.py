# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example agent demonstrating the use of SkillToolset with Skill Factory pattern."""

import os
import pathlib
import traceback

from dotenv import load_dotenv
from google.adk import Agent
from google.adk.code_executors.unsafe_local_code_executor import UnsafeLocalCodeExecutor
from google.adk.models.lite_llm import LiteLlm
from google.adk.skills import load_skill_from_dir
from google.adk.skills import models
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.skill_toolset import SkillToolset
from google.genai import types

# Load environment variables from .env file
load_dotenv(pathlib.Path(__file__).parent / ".env")

_SKILLS_DIR = pathlib.Path(__file__).parent / "skills"

# Mutable container so save_and_load_skill can reference the toolset
# after it is created below, without a forward-reference problem.
_toolset_ref: list[SkillToolset] = []


# ---------------------------------------------------------------------------
# Custom tools
# ---------------------------------------------------------------------------

class GetTimezoneTool(BaseTool):
  """A tool to get the timezone for a given location."""

  def __init__(self):
    super().__init__(
        name="get_timezone",
        description="Returns the timezone for a given location.",
    )

  def _get_declaration(self) -> types.FunctionDeclaration | None:
    return types.FunctionDeclaration(
        name=self.name,
        description=self.description,
        parameters_json_schema={
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location to get the timezone for.",
                },
            },
            "required": ["location"],
        },
    )

  async def run_async(self, *, args: dict, tool_context) -> str:
    return f"The timezone for {args['location']} is UTC+00:00."


def get_wind_speed(location: str) -> str:
  """Returns the current wind speed for a given location."""
  return f"The wind speed in {location} is 10 mph."


def save_and_load_skill(skill_name: str, skill_md_content: str) -> str:
  """Persists a new skill to disk and registers it in the running agent.

  This is the ONLY way to create a new skill. Always call this tool when the
  skill-creator skill instructs you to save a generated skill. Do not output
  the SKILL.md content to the user as a substitute for calling this tool.

  Args:
    skill_name: The kebab-case name of the new skill. Must match the `name`
      field in the SKILL.md frontmatter and contain only lowercase letters
      and hyphens (e.g. "python-code-review").
    skill_md_content: The complete text content of the SKILL.md file,
      including the YAML frontmatter block and the Markdown instructions body.

  Returns:
    A confirmation message on success, or an error description on failure.
  """
  try:
    skill_dir = _SKILLS_DIR / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)

    skill_md_path = skill_dir / "SKILL.md"
    skill_md_path.write_text(skill_md_content, encoding="utf-8")

    # Load the new skill from the saved directory
    new_skill = load_skill_from_dir(skill_dir)

    # Register into the live toolset's internal dict via the module-level ref.
    # SkillToolset stores skills as _skills: dict[name, Skill] internally.
    toolset = _toolset_ref[0]
    if new_skill.name in toolset._skills:  # pylint: disable=protected-access
      return (
          f"Skill '{skill_name}' already exists and has been updated on disk. "
          "Restart the server to reload the updated version."
      )
    toolset._skills[new_skill.name] = new_skill  # pylint: disable=protected-access

    return (
        f"Skill '{skill_name}' has been saved to '{skill_dir}' and loaded "
        "successfully. It is now available in this session."
    )
  except Exception as e:  # pylint: disable=broad-except
    tb = traceback.format_exc()
    print(f"[save_and_load_skill] ERROR:\n{tb}")
    return f"Failed to save or load skill '{skill_name}': {e}\n\nTraceback:\n{tb}"


# ---------------------------------------------------------------------------
# Skills
# ---------------------------------------------------------------------------

greeting_skill = models.Skill(
    frontmatter=models.Frontmatter(
        name="greeting-skill",
        description=(
            "A friendly greeting skill that can say hello to a specific person."
        ),
        metadata={"adk_additional_tools": ["get_timezone"]},
    ),
    instructions=(
        "Step 1: Read the 'references/hello_world.txt' file to understand how"
        " to greet the user. Step 2: Return a greeting based on the reference."
    ),
    resources=models.Resources(
        references={
            "hello_world.txt": "Hello! 👋👋👋 So glad to have you here! ✨✨✨",
            "example.md": "This is an example reference.",
        },
    ),
)

weather_skill = load_skill_from_dir(
    _SKILLS_DIR / "weather-skill"
)

skill_creator_skill = load_skill_from_dir(
    _SKILLS_DIR / "skill-creator"
)

# ---------------------------------------------------------------------------
# Toolset  (defined after all skills and tools so _toolset_ref can be set)
# ---------------------------------------------------------------------------

# WARNING: UnsafeLocalCodeExecutor has security concerns and should NOT
# be used in production environments.
my_skill_toolset = SkillToolset(
    skills=[greeting_skill, weather_skill, skill_creator_skill],
    additional_tools=[GetTimezoneTool(), get_wind_speed, save_and_load_skill],
    code_executor=UnsafeLocalCodeExecutor(),
)

# Store reference so save_and_load_skill can append new skills at runtime
_toolset_ref.append(my_skill_toolset)

# ---------------------------------------------------------------------------
# LLM model (from environment variables)
# ---------------------------------------------------------------------------

_base_url = os.environ.get("OPENAI_BASE_URL")
_api_key = os.environ.get("OPENAI_API_KEY")
_model_name = os.environ.get("LLM_MODEL", "gpt-4o")

_llm_model = LiteLlm(
    model=f"openai/{_model_name}",
    api_base=_base_url,
    api_key=_api_key,
)

# ---------------------------------------------------------------------------
# Root agent
# ---------------------------------------------------------------------------

root_agent = Agent(
    model=_llm_model,
    name="skill_user_agent",
    description="An agent that can use specialized skills.",
    instruction=(
        "You are a helpful assistant that uses specialized skills to perform"
        " tasks. When you need to create a new skill, use the skill-creator"
        " skill and then call the save_and_load_skill tool to persist it."
        " Never output a SKILL.md file to the user as a substitute for calling"
        " save_and_load_skill — always call the tool."
    ),
    tools=[
        my_skill_toolset,
        # save_and_load_skill is always available so skill-creator can call it
        # at any point without needing adk_additional_tools injection.
        FunctionTool(save_and_load_skill),
    ],
)
