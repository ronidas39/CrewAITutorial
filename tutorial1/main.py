from crewai import Agent,Task,Crew,Process
import os
from crewai_tools import SerperDevTool
os.environ["SERPER_API_KEY"]="eb01f53dc754d5bef378e0778ae99de75f4fdd42edf9bf28b441c73cb4bab52b"

search_tool=SerperDevTool()

researcher=Agent(
    role="Senior Researcher",
    goal="uncover top 3 rending news in {topic}",
    verbose=True,
    memory=True,
    backstory=(
        """
    As a research assistant dedicated to uncovering the most impactful trends,
    you're propelled by a relentless curiosity and a commitment to innovation. 
    Your role involves delving deep into the latest developments 
    across various sectors to identify and analyze 
    the top trending news within any given field. 
    This pursuit not only satisfies your thirst for knowledge
    but also enables you to contribute valuable insights that could 
    potentially reshape understandings and expectations on a global scale
    """
    ),
    tools=[search_tool],
    allow_delegation=True
)

blog_writer=Agent(
    role="Expert Writer",
    goal="write compelling contents about {topic}",
    verbose=True,
    memory=True,
    backstory=(
    """
     Armed with the knack for distilling complex subjects into digestible,
    compelling stories, you, as a blog writer, masterfully weave narratives 
    that both enlighten and engage your audience. Your writing illuminates fresh 
    insights and discoveries, making them approachable for everyone. Through your craft,
    you bring to the forefront the essence of new developments across various topics, 
    making the intricate world of news a fascinating journey for your readers.
    """
    ),
    tools=[search_tool],
    allow_delegation=False
)

research_task=Task(
    description=(
    """
    Identify the next big trend in {topic}.
    Focus on identifying pros and cons and the overall narrative.
    Your final report should clearly articulate the key points
    its market opportunities, and potential risks.
    """
    ),
    expected_output="A comprehensive 3 paragraphs long report on the {topic}",
    tools=[search_tool],
    agent=researcher
)

write_task=Task(
    description=(
    """
    Compose an insightful article on {topic}."
    "Focus on the latest trends and how it's impacting the industry."
    "This article should be easy to understand, engaging, and positive.
    """
    ),
    expected_output="A 4 paragraph article on {topic} advancements formatted as markdown",
    tools=[search_tool],
    agent=blog_writer,
    aync_execution=False,
    output_file="blog-post.md"
)
crew=Crew(
    agents=[researcher,blog_writer],
    tasks=[research_task,write_task],
    process=Process.sequential
)

result=crew.kickoff(inputs={"topic":"Latest smart phones"})


