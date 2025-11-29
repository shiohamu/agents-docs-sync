"""
RAG (Retrieval-Augmented Generation) Mixin

ドキュメント生成に必要なコンテキスト情報を
RAGシステムから取得する機能を提供します。
"""


class RAGMixin:
    """RAG機能を提供する Mixin"""

    def _get_rag_context(self, query: str, top_k: int | None = None) -> str:
        """
        RAGコンテキストを取得してフォーマット

        Args:
            query: 検索クエリ
            top_k: 取得するチャンク数（Noneの場合は設定ファイルから読み取る）

        Returns:
            フォーマット済みのコンテキスト文字列（RAG無効時は空文字列）
        """
        # RAGが無効の場合は空文字列を返す
        if not self.config.get("rag", {}).get("enabled", False):
            return ""

        try:
            from docgen.rag.retriever import DocumentRetriever

            self.logger.info(f"Retrieving RAG context for query: {query[:50]}...")

            # top_kが指定されていない場合は設定から取得
            if top_k is None:
                top_k = self.config.get("rag", {}).get("retrieval", {}).get("top_k", 6)

            # Retrieverを使用してコンテキストを取得
            retriever = DocumentRetriever(self.config, self.project_root)
            chunks = retriever.retrieve(query, top_k=top_k)

            if not chunks:
                self.logger.warning("No relevant chunks found for query")
                return ""

            # コンテキストをフォーマット
            formatted_context = retriever.format_context(chunks)

            self.logger.info(f"Retrieved {len(chunks)} relevant chunks")
            return formatted_context

        except ImportError:
            self.logger.warning(
                "RAGモジュールが利用できません。"
                "RAG依存関係をインストールしてください: uv sync --extra rag"
            )
            return ""
        except FileNotFoundError as e:
            self.logger.warning(
                f"RAGインデックスが見つかりません: {e}。"
                "インデックスをビルドしてください: uv run python -m docgen.docgen --build-index"
            )
            return ""
        except Exception as e:
            self.logger.error(f"RAGコンテキスト取得中にエラー: {e}", exc_info=True)
            return ""
