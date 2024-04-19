# Define the Streamlit app
import streamlit as st
#from app import *

def main():
    # Set the title of the app
    st.title("Blog Post Summary Generator")

    # Collect inputs from the user
    feed_url = st.text_input("Enter the feed URL:")
    api_key = st.text_input("Enter the Generative AI API key:")
    model_name = st.text_input("Enter the Generative AI model name:")
    connection_string = st.text_input("Enter the Azure Blob Storage connection string:")
    container_name = st.text_input("Enter the name of the container in Azure Blob Storage:")

    # Generate the article list and blog post summaries
    """ if st.button("Generate Summaries"):
        # Configure the generative AI model
        model = configure_generative_ai(api_key, model_name)

        # Generate the article list
        articles = generate_article_list(feed_url)

        # Generate the blog post summaries
        summary_list = []
        for article in articles:
            url = article[1]
            prompt_parts = [
                f"Imagine you are a technical architect with expertise in summarizing blog content. You have been given a URL {url} of a blog post. Your task is to distill the essence of the blog post into a concise summary, not exceeding 150 words. The summary should be comprehensive, capturing all the relevant content from the blog post. Begin with the title of the blog hyperlinking it to the url, followed by the summary presented as bullet points. Remember, the goal is to provide a quick glance at the blog's content without losing any significant information. Your summary should be formal and confident, reflecting your expertise. The expected result format is markdown(md). Use your creativity and originality to make the summary engaging and informative."
            ]
            summary = generate_blog_post_summary(model, prompt_parts)
            summary_list.append((article[0], url, summary))

        # Write the summary list to a markdown file
        today = datetime.now().strftime("%d%m%Y")
        markdown_file_path = f"summary_list_{today}.md"
        with open(markdown_file_path, 'w', encoding='utf-8') as file:
            file.write("# Cloudy with a Chance of AI\n\n")
            file.write("Immerse yourself in Sumanth Badethalav's **Cloudy with a Chance of AI**, your curated lightning bolt of knowledge, condensing top AI and cloud blog highlights into an electrifying summary. \n\n")
            for summary in summary_list:
                file.write(f"{summary[2]}\n\n")

        # Upload the summary markdown file to Azure Blob Storage
        blob_name = f"summaries/{markdown_file_path}"
        upload_summary_to_blob_storage(connection_string, container_name, blob_name, markdown_file_path)

        # Display the generated summaries
        st.subheader("Generated Summaries")
        for summary in summary_list:
            st.markdown(f"**Title:** {summary[0]}")
            st.markdown(f"**URL:** {summary[1]}")
            st.markdown(f"**Summary:**")
            st.markdown(summary[2])
            st.markdown("---") """

# Run the Streamlit app
if __name__ == "__main__":
    main()