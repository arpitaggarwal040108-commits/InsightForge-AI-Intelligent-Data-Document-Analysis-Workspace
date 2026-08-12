def get_prompt_template(doc_type):

    if doc_type == "resume":

        return """
        Answer in this format:

        ### Name

        ### Skills

        ### Experience

        ### Projects

        ### Education
        """

    elif doc_type == "research_paper":

        return """
        Answer in this format:

        ## Objective

        ## Methodology

        ## Results

        ## Conclusion
        """

    else:

        return """
        Use clean Markdown formatting.
        """