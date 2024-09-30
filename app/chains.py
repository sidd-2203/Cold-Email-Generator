import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()



class Chain:
    def __init__(self):
        self.llm=ChatGroq(model="llama3-70b-8192",api_key=os.getenv('GROQ_API_KEY'),temperature=0,max_tokens=None,timeout=None,max_retries=2)
    
    def extract_jobs(self,cleaned_text):
        prompt_extract=PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}

            ### INSTRUCTION:
            The scraped text is from the careers page of a website.
            Your job is to extract the job posting and return them in JSON format containing following roles:
            `role`,`experience`,`skills` and `description`. 
            Only return the valid JSON
            ### VALID JSON ONLY (NO PREAMBLE): 
            """
        )

        chain_extract=prompt_extract| self.llm
        res=chain_extract.invoke(input={'page_data':cleaned_text})
        print(res.content)
        try:
            json_parser=JsonOutputParser()
            res=json_parser.parse(res.content)  
        except OutputParserException:
            raise OutputParserException('Context too big, Unable to parse to Json')
        
        return res if isinstance(res,list) else [res]

    def write_email(self,job,links):
        prompt_email=PromptTemplate.from_template(
            '''
            ### JOB_DESCRIPTION:
            {job_description}
            ### INSTRUCTION:
            You are Siddharth, a student from final year BTech -MTech(Integrated) Computer Science student at LNMIIT Jaipur college who is well versed
            in Android Development, Web Development and even Full stack development and is currently working on use of llms.
            During my coding journey you have won various acheievements and been a part of Google Summer of code 2023 at NRNB worked under an Harvard Professor
            and also interned at Deloitte which is a big four.
            Your job is to write a cold email to the recruiter regarding the job mentioned above in fullfiling their needs.
            Also add the most relevant links from the following to showcase the work done by you: {portfolio_links}
            Remember you are Siddharth a prefinal student.
            DO NOT PROVIDE PREAMBLE
            ### EMAIL ONLY (NO PREAMBLE):
            
            '''
        )
        email_chain= prompt_email | self.llm
        res=email_chain.invoke(input={'job_description':str(job),"portfolio_links":links})
        # print(res.content)
        return res.content


