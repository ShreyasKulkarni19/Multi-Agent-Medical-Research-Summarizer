from graph_config import compiled
from data.cache_utils import get_cached_result, store_result_in_cache
from utils.pdf_generator import generate_medical_research_pdf

from logging_config import setup_logging
import logging
import json
import warnings
warnings.filterwarnings("ignore")

setup_logging()
logger = logging.getLogger(__name__)


def run_pipeline(query: str):
    logger.info(f"Running pipeline for query: {query}")
    cached = get_cached_result(query)

    if cached:
        
        logger.info(f"[CACHE] Query hit: {query}")
        logger.info(f"[CACHE] Loaded cached result for query: {query}")
        logger.info(cached["final_output"])
        
        # Generate PDF for cached result as well
        try:
            pdf_success = generate_medical_research_pdf(cached["final_output"])
            if pdf_success:
                logger.info("PDF report generated successfully from cache")
            else:
                logger.error("Failed to generate PDF report from cache")
        except Exception as e:
            logger.error(f"Error generating PDF from cache: {str(e)}")
        
        return cached["final_output"]

    logger.info(f"[GRAPH] Running full pipeline for query: {query}")
    logger.info(f"[+] Running graph for new query: {query}")
    initial_state = {"query": query}
    result = compiled.invoke(initial_state)

    logger.info("storing result in cache...")
    store_result_in_cache(query, result)
    print(result["final_output"])
    
    logger.info("stored result in cache")
    
    # Save JSON output
    with open("output.json", "w") as f:
        json.dump(result["final_output"], f, indent=2)
    
    # Generate PDF output
    try:
        pdf_success = generate_medical_research_pdf(result["final_output"])
        if pdf_success:
            logger.info("PDF report generated successfully")
        else:
            logger.error("Failed to generate PDF report")
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
    
    return result["final_output"]


def main():
    """Main interactive function to get user input and run the pipeline"""
    print("=" * 65)
    print("    Welcome to the Medical Research Summarizer!")
    print("=" * 65)
    print("This AI system will help you learn about medical conditions")
    print("by finding and summarizing the latest research papers.")
    print()
    print("Examples of queries you can try:")
    print("- 'Tell me about diabetes'")
    print("- 'Latest research on brain cancer'")
    print("- 'What are new treatments for heart disease?'")
    print("=" * 65)
    
    while True:
        try:
            # Get user input
            query = input("\nWhat would you like to learn about today? (or type 'quit' to exit): ").strip()
            
            # Check if user wants to quit
            if query.lower() in ['quit', 'exit', 'q', 'bye', 'stop']:
                print("\nThank you for using the Medical Research Summarizer!")
                print("Stay healthy and keep learning!")
                break
            
            # Check if input is empty
            if not query:
                print("Please enter a medical condition or topic you'd like to learn about.")
                continue
            
            # Check for very short queries
            if len(query.split()) < 2:
                print("Please provide a more detailed query for better results.")
                print("Example: Instead of 'cancer', try 'liver cancer treatments'")
                continue
            
            # Run the pipeline
            print(f"\nSearching for research on: '{query}'")
            print("This may take a few moments while we:")
            print("  1. Search for relevant papers")
            print("  2. Classify and analyze documents")
            print("  3. Generate summaries")
            print("  4. Create PDF report")
            print("-" * 50)
            
            result = run_pipeline(query)
            
            print("\n" + "=" * 50)
            print("Research summary completed successfully!")
            print("Files generated:")
            print("  - JSON results saved to 'output.json'")
            print("  - PDF report saved to current directory")
            print("=" * 50)
            
            # Ask if user wants another search
            another = input("\nWould you like to search for another topic? (y/n): ").strip().lower()
            if another not in ['y', 'yes', 'yeah', 'yep', '1']:
                print("\nThank you for using the Medical Research Summarizer!")
                print("Stay healthy and keep learning!")
                break
                
        except KeyboardInterrupt:
            print("\n\nProcess interrupted by user.")
            print("Thank you for using the Medical Research Summarizer!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try again with a different query.")
            continue

if __name__ == "__main__":
    main()

    
