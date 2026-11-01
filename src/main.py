import os
from dotenv import load_dotenv
from openai import OpenAI
from seo_workflow import SEOWorkflow

load_dotenv()

def main():
    print("WELCOME TO YOUR AUTONOMOUS SEO AGENCY")
    print("=====================================")

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("OpenAI API key is not configured.")
        return

    client = OpenAI(api_key=api_key)
    print("OpenAI connection is configured successfully.")

    workflow = SEOWorkflow()
    workflow.show_workflow()


if __name__ == "__main__":
    main()
