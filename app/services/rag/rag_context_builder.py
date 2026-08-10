class RAGContextBuilder:

    def build_context(
        self,
        search_results: list[dict],
    ) -> str:

        if not search_results:
            return ""

        context_parts = []

        for result in search_results:

            context_parts.append(
                f"""
--- CHUNK {result['chunk_index']} ---

{result['content']}
"""
            )

        return "\n".join(context_parts)