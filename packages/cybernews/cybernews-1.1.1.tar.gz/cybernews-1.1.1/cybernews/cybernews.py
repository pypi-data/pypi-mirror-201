"""
    Main Class for Extracting News
"""
from utils.extractor import Extractor


class CyberNews:

    def __init__(self) -> None:
        self._extractor = Extractor()
        self._news_types = [
            {
                "general": [
                    {
                        "https://ciosea.economictimes.indiatimes.com/news/next-gen-technologies": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    },
                    {
                        "https://telecom.economictimes.indiatimes.com/news/internet": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    }
                ],
            },
            {
                "dataBreach": [
                    {
                        "https://thehackernews.com/search/label/data%20breach": {
                            "headlines": "h2.home-title",
                            "author": ".item-label span",
                            "fullNews": ".home-desc",
                            "newsImg": ".img-ratio img",
                            "newsURL": "a.story-link",
                            "date": ".item-label",
                        }
                    },
                    {
                        "https://ciso.economictimes.indiatimes.com/tag/data+breaches": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    },
                ],
            },
            {
                "cyberAttack": [
                    {
                        "https://thehackernews.com/search/label/Cyber%20Attack": {
                            "headlines": "h2.home-title",
                            "author": ".item-label span",
                            "fullNews": ".home-desc",
                            "newsImg": ".img-ratio img",
                            "newsURL": "a.story-link",
                            "date": ".item-label",
                        }
                    },
                    {
                        "https://ciso.economictimes.indiatimes.com/news/cyberwarfare": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    },
                ],
            },
            {
                "vulnerability": [
                    {
                        "https://thehackernews.com/search/label/Vulnerability": {
                            "headlines": "h2.home-title",
                            "author": ".item-label span",
                            "fullNews": ".home-desc",
                            "newsImg": ".img-ratio img",
                            "newsURL": "a.story-link",
                            "date": ".item-label",
                        }
                    },
                    {
                        "https://ciso.economictimes.indiatimes.com/news/email-security": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    },
                ],
            },
            {
                "malware": [
                    {
                        "https://thehackernews.com/search/label/Malware": {
                            "headlines": "h2.home-title",
                            "author": ".item-label span",
                            "fullNews": ".home-desc",
                            "newsImg": ".img-ratio img",
                            "newsURL": "a.story-link",
                            "date": ".item-label",
                        }
                    }
                ]
            },
            {
                "security": [
                    {
                        "https://ciosea.economictimes.indiatimes.com/news/security": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    },
                    {
                        "https://telecom.economictimes.indiatimes.com/tag/hacking": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    },
                ]
            },
            {
                "cloud": [
                    {
                        "https://ciosea.economictimes.indiatimes.com/news/cloud-computing": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    }
                ]
            },
            {
                "tech": [
                    {
                        "https://ciosea.economictimes.indiatimes.com/news/consumer-tech": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    },
                ]
            },
            {
                "iot": [
                    {
                        "https://ciosea.economictimes.indiatimes.com/news/internet-of-things": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    },
                ]
            },
            {
                "bigData": [
                    {
                        "https://ciosea.economictimes.indiatimes.com/news/big-data": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    },
                    {
                        "https://ciosea.economictimes.indiatimes.com/news/data-center": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    },
                ]
            },
            {
                "business": [
                    {
                        "https://ciosea.economictimes.indiatimes.com/news/business-analytics": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    }
                ]
            },
            {
                "mobility": [
                    {
                        "https://ciosea.economictimes.indiatimes.com/tag/mobility": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    }
                ]
            },
            {
                "research": [
                    {
                        "https://ciosea.economictimes.indiatimes.com/tag/research": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    }
                ]
            },
            {
                "socialMedia": [
                    {
                        "https://telecom.economictimes.indiatimes.com/search/social": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    }
                ]
            },
            {
                "corporate": [
                    {
                        "https://ciosea.economictimes.indiatimes.com/news/corporate": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    },
                    {
                        "https://telecom.economictimes.indiatimes.com/news/industry": {
                            "headlines": ".descBx h3 a",
                            "author": ".metaTx",
                            "fullNews": ".descBx p",
                            "newsImg": "figure.avtar a img",
                            "newsURL": ".descBx a",
                            "date": None,
                        }
                    }
                ]
            },
        ]

    @property
    def get_news_types(self) -> list:
        return [news_type for news in self._news_types for news_type, _ in news.items()]

    def get_news(self, news) -> list:
        for news_type in self._news_types:
            if news in news_type:
                try:
                    return self._extractor.data_extractor(news_type[news])
                except Exception as e:
                    raise Exception(
                        f"An error occurred while processing the news of type: '{news}': {str(e)}")
        raise ValueError(f"News type '{news}' not found")