class RAGContextBuilder:

    def build_context(
        self,
        search_results: list[dict],
    ) -> str:

        if not search_results:
            return ""

        context_parts = []

        for rank, result in enumerate(
            search_results,
            start=1,
        ):

            chunk_index = result["chunk_index"]
            content = result["content"]

            similarity = result.get(
                "similarity",
                0.0,
            )

            context_parts.append(
                f"""--- SOURCE {rank} ---
Chunk: {chunk_index}
Relevance Score: {similarity:.4f}

{content}
"""
            )

        return "\n".join(context_parts)