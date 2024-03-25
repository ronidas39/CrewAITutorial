import os
from crewai import Agent,Task,Crew,Process
from crewai_tools import SerperDevTool



os.environ["SERPER_API_KEY"] = "eb01f53dc754d5bef378e0778ae99de75f4fdd42edf9bf28b441c73cb4bab52b" # serper.dev API key

search_tool = SerperDevTool()

# Creating a senior researcher agent with memory and verbose mode
researcher = Agent(
  role='Senior Researcher',
  goal='Uncover top 3 trending news in {topic}',
  verbose=True,
  memory=True,
  backstory=(
    """
    """
  ),
  tools=[search_tool],
  allow_delegation=True
)

# Creating a writer agent with custom tools and delegation capability
writer = Agent(
  role='Writer',
  goal='Narrate compelling stories about {topic}',
  verbose=True,
  memory=True,
  backstory=(
    """
    """
  ),
  tools=[search_tool],
  allow_delegation=False
)


# Research task
research_task = Task(
  description=(
    "Identify the next big trend in {topic}."
    "Focus on identifying pros and cons and the overall narrative."
    "Your final report should clearly articulate the key points"
    "its market opportunities, and potential risks."
  ),
  expected_output='A comprehensive 3 paragraphs long report on the latest AI trends.',
  tools=[search_tool],
  agent=researcher,
)

# Writing task with language model configuration
write_task = Task(
  description=(
    "Compose an insightful article on {topic}."
    "Focus on the latest trends and how it's impacting the industry."
    "This article should be easy to understand, engaging, and positive."
  ),
  expected_output='A 4 paragraph article on {topic} advancements formatted as markdown.',
  tools=[search_tool],
  agent=writer,
  async_execution=False,
  output_file='new-blog-post.md'  # Example of output customization
)


# Forming the tech-focused crew with enhanced configurations
crew = Crew(
  agents=[researcher, writer],
  tasks=[research_task, write_task],
  process=Process.sequential  # Optional: Sequential task execution is default
)
result = crew.kickoff(inputs={'topic': 'AI in smartphones'})
print(result)
