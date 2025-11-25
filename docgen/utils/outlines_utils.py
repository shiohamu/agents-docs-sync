"""
Outlines統合ユーティリティモジュール
共通のOutlines関連機能をまとめる
"""

try:
    import outlines

    OUTLINES_AVAILABLE = True
except ImportError:
    OUTLINES_AVAILABLE = False
    outlines = None

from typing import Any

from ..utils.llm_client import LLMClientFactory


def should_use_outlines(config: dict[str, Any]) -> bool:
    """
    Outlinesを使用するかどうかを判定

    Args:
        config: 設定辞書

    Returns:
        Outlinesを使用するかどうか
    """
    # 設定でOutlinesが有効になっているかチェック
    return config.get("use_outlines", False) and OUTLINES_AVAILABLE


def create_outlines_model(client, provider: str = "openai"):
    """
    Outlinesモデルを作成

    Args:
        client: LLMクライアント
        provider: プロバイダー名 ('openai', 'anthropic', 'local')

    Returns:
        Outlinesモデルインスタンス（作成できない場合はNone）
    """
    if not OUTLINES_AVAILABLE:
        return None

    try:
        # クライアントの種類に応じてOutlinesモデルを作成
        if hasattr(client, "client") and hasattr(client.client, "api_key"):
            # OpenAIクライアント
            return outlines.from_openai(client.client, client.model)
        elif hasattr(client, "base_url"):
            # ローカルLLMクライアント
            provider = getattr(client, "provider", "ollama")

            if provider == "ollama":
                # Ollamaの場合
                return outlines.from_ollama(client.model, client.base_url)
            elif provider == "lmstudio":
                # LM StudioはOpenAI互換だが、Outlinesとの互換性が不十分
                # 従来のLLM生成を使用
                return outlines.from_llamacpp(client.model)
            else:
                # その他のローカルLLMはOpenAI互換APIとして扱う
                import openai

                openai_client = openai.OpenAI(
                    base_url=client.base_url,
                    api_key="dummy",  # ローカルでは不要
                )
                return outlines.from_openai(openai_client, client.model)
        else:
            raise ValueError("サポートされていないクライアントタイプ")
    except Exception:
        # エラーログは呼び出し元で処理
        return None


def get_llm_client_with_fallback(config: dict[str, Any], agents_config: dict[str, Any]):
    """
    LLMクライアントを取得（フォールバック付き）

    Args:
        config: メイン設定
        agents_config: AGENTS設定

    Returns:
        LLMクライアントインスタンス
    """
    llm_mode = agents_config.get("llm_mode", "api")
    preferred_mode = "api" if llm_mode in ["api", "both"] else "local"

    return LLMClientFactory.create_client_with_fallback(
        agents_config, preferred_mode=preferred_mode
    )


def clean_llm_output(text: str) -> str:
    """
    LLMの出力から思考過程や試行錯誤の痕跡を削除

    Args:
        text: LLMで生成されたテキスト

    Returns:
        クリーンアップされたテキスト
    """
    if not text:
        return text

    lines = text.split("\n")
    cleaned_lines = []
    in_code_block = False
    code_block_lang = None

    i = 0
    while i < len(lines):
        line = lines[i]

        # コードブロックの開始/終了を検出
        if line.strip().startswith("```"):
            if not in_code_block:
                in_code_block = True
                code_block_lang = line.strip()[3:].strip().lower()
                # マークダウンコードブロック内の思考過程をスキップ
                if "markdown" in code_block_lang:
                    i += 1
                    # 次の```までスキップ
                    while i < len(lines) and not lines[i].strip().startswith("```"):
                        i += 1
                    if i < len(lines):
                        i += 1  # ```をスキップ
                    in_code_block = False
                    continue
                else:
                    cleaned_lines.append(line)
                    i += 1
                    continue
            else:
                in_code_block = False
                code_block_lang = None
                cleaned_lines.append(line)
                i += 1
                continue

        # コードブロック内はそのまま保持
        if in_code_block:
            cleaned_lines.append(line)
            i += 1
            continue

        # 思考過程のパターンを検出
        line_lower = line.lower().strip()

        # 特殊なマーカーパターン（最初にチェック）
        if "<|channel|>" in line or "<|message|>" in line or "commentary/analysis" in line_lower:
            i += 1
            # 次の空行または通常のコンテンツまでスキップ
            while (
                i < len(lines)
                and not lines[i].strip().startswith("##")
                and not lines[i].strip().startswith("<!--")
            ):
                if lines[i].strip() and not any(
                    pattern in lines[i].lower()
                    for pattern in ["let's", "we need", "but we", "thus final"]
                ):
                    break
                i += 1
            continue

        # 思考過程の開始パターン
        thinking_patterns = [
            "we need to",
            "thus final answer",
            "let's generate",
            "let's do",
            "but we need",
            "hence final answer",
            "thus final output",
            "i will produce",
            "i think",
            "ok i'll",
            "let's finalize",
            "but i think",
            "but we need to",
            "thus final answer will",
            "we should produce",
            "we will output",
            "we must produce",
            "thus the final",
            "but the actual",
            "so i will",
            "i'm going to",
            "i'm still not sure",
            "but it's enough",
            "let's output",
            "let's produce",
            "let's final answer",
            "but we need the final",
            "thus final answer is",
            "we now produce",
            "this content includes",
            "but we also mention",
            "ok, i will",
            "thus we must",
            "but we need to ensure",
            "let's generate:",
            "we should produce final",
            "thus final answer will be",
            "but i'm still not sure",
            "but i think it's",
            "let's finalize:",
            "we need the final answer",
            "thus final answer:",
            "ok i'll produce",
            "以下が、",
            "改訂版です",
            "手動セクションは保持",
            "we should now",
            "we will not include",
            "should we keep",
            "possibly they want",
            "but we must keep",
            "but we might need",
            "however, user wrote",
            "also note",
            "but the user",
            "ok final output",
            "ok. i'll generate",
            "let's create final output",
            "check that it doesn't",
            "now i will provide",
            "the user wants",
            "they gave",
            "so we should",
            "so we can",
            "also keep",
            "we must not include",
            "so final output",
            "but we must also keep",
            "we must only output",
            "but we must",
        ]

        # 思考過程の行をスキップ
        if any(pattern in line_lower for pattern in thinking_patterns):
            i += 1
            continue

        # プレースホルダーや不完全な記述を検出
        placeholder_patterns = [
            "???",
            "(??)",
            "... ...",
            "|  | |",
            "---‐‐‐",
            "continue",
            "we should now",
            "this content, while present",
            "# ... (continue)",
        ]

        if any(pattern in line_lower for pattern in placeholder_patterns):
            i += 1
            continue

        # 空行の連続を制限（3行以上は2行に）
        if not line.strip():
            if cleaned_lines and not cleaned_lines[-1].strip():
                if len(cleaned_lines) >= 2 and not cleaned_lines[-2].strip():
                    i += 1
                    continue

        cleaned_lines.append(line)
        i += 1

    # 結果を結合
    result = "\n".join(cleaned_lines)

    # 先頭と末尾の空行を削除
    result = result.strip()

    # 重複した説明を削除（同じ行が3回以上続く場合）
    lines_result = result.split("\n")
    deduplicated = []
    prev_line = None
    repeat_count = 0

    for line in lines_result:
        if line == prev_line:
            repeat_count += 1
            if repeat_count < 3:
                deduplicated.append(line)
        else:
            repeat_count = 0
            deduplicated.append(line)
        prev_line = line

    return "\n".join(deduplicated)


def validate_output(text: str) -> bool:
    """
    LLMの出力を検証して、不適切な内容が含まれていないかチェック

    Args:
        text: 検証するテキスト

    Returns:
        検証に合格したかどうか
    """
    if not text or not text.strip():
        return False

    text_lower = text.lower()

    # 特殊なマーカーパターンをチェック
    if "<|channel|>" in text or "<|message|>" in text or "commentary/analysis" in text_lower:
        return False

    # 思考過程のパターンが含まれていないかチェック
    thinking_patterns = [
        "thus final answer",
        "let's generate",
        "but we need",
        "i will produce",
        "i think",
        "let's finalize",
        "we should produce",
        "we will output",
        "thus the final",
        "i'm going to",
        "let's output",
        "let's produce",
        "but i think it's",
        "thus final answer will be",
        "以下が、",
        "改訂版です",
        "we should now",
        "we will not include",
        "should we keep",
        "possibly they want",
        "but we must keep",
        "but we might need",
        "however, user wrote",
        "also note",
        "but the user",
        "ok final output",
        "ok. i'll generate",
        "let's create final output",
        "check that it doesn't",
        "now i will provide",
        "the user wants",
        "they gave",
        "so we should",
        "so we can",
        "also keep",
        "we must not include",
        "so final output",
        "but we must also keep",
        "we must only output",
        "but we must",
    ]

    for pattern in thinking_patterns:
        if pattern in text_lower:
            return False

    # プレースホルダーが含まれていないかチェック
    placeholder_patterns = [
        "???",
        "(??)",
        "... ...",
        "|  | |",
        "---‐‐‐",
        "# ... (continue)",
    ]

    for pattern in placeholder_patterns:
        if pattern in text:
            return False

    # マークダウンコードブロック内に思考過程が含まれていないかチェック
    lines = text.split("\n")
    in_markdown_block = False
    for line in lines:
        if line.strip().startswith("```"):
            lang = line.strip()[3:].strip().lower()
            if "markdown" in lang:
                in_markdown_block = True
            elif in_markdown_block:
                in_markdown_block = False
        elif in_markdown_block:
            if any(pattern in line.lower() for pattern in thinking_patterns):
                return False

    return True
