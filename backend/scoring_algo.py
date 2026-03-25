"""
Credibility scoring algorithm for articles.
Uses weighted sum approach to calculate a final credibility score out of 100.
"""


def calculate_credibility_score(article_data: dict) -> float:
    """
    Calculate the credibility score of an article using a weighted sum algorithm.

    Args:
        article_data: Dictionary containing:
            - citation_count (int): Number of citations in the article
            - has_author_credentials (bool): Whether author has relevant credentials
            - emotional_language_score (float): Score from 0.0 (no emotion) to 1.0 (highly emotional)

    Returns:
        float: Final credibility score out of 100

    Weights:
        - citation_count: 40%
        - has_author_credentials: 30%
        - emotional_language_score: 30% (inverted, lower emotion = higher credibility)
    """

    # Extract input values
    citation_count = article_data.get("citation_count", 0)
    has_author_credentials = article_data.get("has_author_credentials", False)
    emotional_language_score = article_data.get("emotional_language_score", 0.5)

    # Validate emotional language score is in range [0.0, 1.0]
    emotional_language_score = max(0.0, min(1.0, emotional_language_score))

    # Weight 1: Citation Count (40%)
    # Normalize citation count to 0-100 scale
    # Assumption: 0 citations = 0 points, 10+ citations = 100 points (diminishing return)
    citation_score = min(100, citation_count * 10)
    citation_weight = 0.40

    # Weight 2: Author Credentials (30%)
    # Boolean: 100 points if has credentials, 0 if not
    credentials_score = 100 if has_author_credentials else 0
    credentials_weight = 0.30

    # Weight 3: Emotional Language (30%)
    # Lower emotional language = higher credibility
    # Inverted: 1.0 emotion = 0 points, 0.0 emotion = 100 points
    emotional_score = (1.0 - emotional_language_score) * 100
    emotion_weight = 0.30

    # Calculate weighted sum
    final_score = (
        (citation_score * citation_weight)
        + (credentials_score * credentials_weight)
        + (emotional_score * emotion_weight)
    )

    # Clamp final score to 0-100 range
    final_score = max(0.0, min(100.0, final_score))

    return final_score


# Example usage
if __name__ == "__main__":
    # Example article data
    example_article = {
        "citation_count": 8,
        "has_author_credentials": True,
        "emotional_language_score": 0.2,
    }

    score = calculate_credibility_score(example_article)
    print(f"Article credibility score: {score:.2f}/100")
