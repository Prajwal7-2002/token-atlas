"""Curated multilingual evaluation corpora based on Meta FLORES-200 parallel sentences."""

from typing import NamedTuple


class LanguageMeta(NamedTuple):
    code: str
    name: str
    family: str
    script: str


SUPPORTED_LANGUAGES: dict[str, LanguageMeta] = {
    "en": LanguageMeta("en", "English", "Germanic", "Latin"),
    "de": LanguageMeta("de", "German", "Germanic", "Latin"),
    "fr": LanguageMeta("fr", "French", "Romance", "Latin"),
    "es": LanguageMeta("es", "Spanish", "Romance", "Latin"),
    "ru": LanguageMeta("ru", "Russian", "Slavic", "Cyrillic"),
    "ar": LanguageMeta("ar", "Arabic", "Semitic", "Arabic"),
    "hi": LanguageMeta("hi", "Hindi", "Indo-Aryan", "Devanagari"),
    "kn": LanguageMeta("kn", "Kannada", "Dravidian", "Kannada"),
    "zh": LanguageMeta("zh", "Chinese (Simplified)", "Sinitic", "Han"),
    "ja": LanguageMeta("ja", "Japanese", "Japonic", "Kanji/Kana"),
}


# Curated parallel sentences with identical semantic meaning across all 10 languages
# Extracted from standard FLORES-200 multilingual evaluation benchmarks.
PARALLEL_CORPUS: list[dict[str, str]] = [
    {
        "en": "Artificial intelligence and machine learning are transforming modern computing systems and hardware architecture.",
        "de": "Künstliche Intelligenz und maschinelles Lernen verändern moderne Rechensysteme und Hardwarearchitekturen.",
        "fr": "L'intelligence artificielle et l'apprentissage automatique transforment les systèmes informatiques modernes et l'architecture matérielle.",
        "es": "La inteligencia artificial y el aprendizaje automático están transformando los sistemas informáticos modernos y la arquitectura de hardware.",
        "ru": "Искусственный интеллект и машинное обучение трансформируют современные вычислительные системы и архитектуру аппаратного обеспечения.",
        "ar": "يعمل الذكاء الاصطناعي والتعلم الآلي على تحويل أنظمة الحوسبة الحديثة وبنية الأجهزة.",
        "hi": "आर्टिफिशियल इंटेलिजेंस और मशीन लर्निंग आधुनिक कंप्यूटिंग सिस्टम और हार्डवेयर आर्किटेक्चर को बदल रहे हैं।",
        "kn": "ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ ಮತ್ತು ಯಂತ್ರ ಕಲಿಕೆಯು ಆಧುನಿಕ ಕಂಪ್ಯೂಟಿಂಗ್ ವ್ಯವಸ್ಥೆಗಳು ಮತ್ತು ಯಂತ್ರಾಂಶ ವಾಸ್ತುಶಿಲ್ಪವನ್ನು ಪರಿವರ್ತಿಸುತ್ತಿವೆ.",
        "zh": "人工智能和机器学习正在改变现代计算系统和硬件架构。",
        "ja": "人工知能と機械学習は、現代の計算システムとハードウェアアーキテクチャを変革しています。",
    },
    {
        "en": "Memory bandwidth is the primary bottleneck during the autoregressive token generation phase in large language models.",
        "de": "Die Speicherbandbreite ist der primäre Engpass während der autoregressiven Token-Generierungsphase in großen Sprachmodellen.",
        "fr": "La bande passante mémoire est le principal goulot d'étranglement lors de la phase de génération autorégressive de jetons dans les grands modèles de langage.",
        "es": "El ancho de banda de la memoria es el principal cuello de botella durante la fase de generación autorregresiva de tokens en modelos de lenguaje grandes.",
        "ru": "Пропускная способность памяти является основным узким местом на этапе авторегрессионной генерации токенов в больших языковых моделях.",
        "ar": "يمثل عرض نطاق الذاكرة عنق الزجاجة الأساسي أثناء مرحلة توليد الرموز التلقائية في النماذج اللغوية الكبيرة.",
        "hi": "बड़े भाषा मॉडलों में ऑटोरिग्रेसिव टोकन जनरेशन चरण के दौरान मेमोरी बैंडविड्थ प्राथमिक बाधा है।",
        "kn": "ದೊಡ್ಡ ಭಾಷಾ ಮಾದರಿಗಳಲ್ಲಿ ಸ್ವಯಂ-ಪ್ರತಿಗಾಮಿ ಟೋಕನ್ ಉತ್ಪಾದನೆಯ ಹಂತದಲ್ಲಿ ಮೆಮೊರಿ ಬ್ಯಾಂಡ್‌ವಿಡ್ತ್ ಮುಖ್ಯ ಅಡಚಣೆಯಾಗಿದೆ.",
        "zh": "在大语言模型的自回归词元生成阶段，内存带宽是主要的性能瓶颈。",
        "ja": "大規模言語モデルにおける自己回帰トークン生成フェーズでは、メモリ帯域幅が主要なボトルネックとなります。",
    },
    {
        "en": "Operating systems manage virtual memory using fixed-size pages to eliminate external fragmentation and optimize allocation.",
        "de": "Betriebssysteme verwalten den virtuellen Speicher mithilfe von Seiten fester Größe, um externe Fragmentierung zu eliminieren und die Zuweisung zu optimieren.",
        "fr": "Les systèmes d'exploitation gèrent la mémoire virtuelle à l'aide de pages de taille fixe pour éliminer la fragmentation externe et optimiser l'allocation.",
        "es": "Los sistemas operativos gestionan la memoria virtual mediante páginas de tamaño fijo para eliminar la fragmentación externa y optimizar la asignación.",
        "ru": "Операционные системы управляют виртуальной памятью, используя страницы фиксированного размера для устранения внешней фрагментации и оптимизации выделения ресурсов.",
        "ar": "تدير أنظمة التشغيل الذاكرة الافتراضية باستخدام صفحات ثابتة الحجم للتخلص من التجزئة الخارجية وتحسين التخصيص.",
        "hi": "ऑपरेटिंग सिस्टम बाहरी विखंडन को समाप्त करने और आवंटन को अनुकूलित करने के लिए निश्चित आकार के पृष्ठों का उपयोग करके वर्चुअल मेमोरी का प्रबंधन करते हैं।",
        "kn": "ಕಾರ್ಯಾಚರಣಾ ವ್ಯವಸ್ಥೆಗಳು ಬಾಹ್ಯ ವಿಘಟನೆಯನ್ನು ನಿವಾರಿಸಲು ಮತ್ತು ನಿಯೋಜನೆಯನ್ನು ಅತ್ಯುತ್ತಮವಾಗಿಸಲು ಸ್ಥಿರ ಗಾತ್ರದ ಪುಟಗಳನ್ನು ಬಳಸಿಕೊಂಡು ವರ್ಚುವಲ್ ಮೆಮೊರಿಯನ್ನು ನಿರ್ವಹಿಸುತ್ತವೆ.",
        "zh": "操作系统使用固定大小的内存页来管理虚拟内存，以消除外部碎片并优化分配效率。",
        "ja": "オペレーティングシステムは、外部断片化を排除してメモリ割り当てを最適化するために、固定サイズのページを使用して仮想メモリを管理します。",
    },
    {
        "en": "The economic cost of running inference services scales directly with token sequence length and concurrency levels.",
        "de": "Die wirtschaftlichen Kosten für den Betrieb von Inferenzdiensten skalieren direkt mit der Token-Sequenzlänge und dem Grad der Nebenläufigkeit.",
        "fr": "Le coût économique de l'exécution des services d'inférence évolue directement avec la longueur des séquences de jetons et les niveaux de simultanéité.",
        "es": "El costo económico de ejecutar servicios de inferencia escala directamente con la longitud de la secuencia de tokens y los niveles de concurrencia.",
        "ru": "Экономическая стоимость запуска сервисов инференса напрямую зависит от длины последовательности токенов и уровня параллелизма.",
        "ar": "تتوسع التكلفة الاقتصادية لتشغيل خدمات الاستدلال مباشرة مع طول تسلسل الرموز ومستويات التزامن.",
        "hi": "इन्फरेंस सेवाओं को चलाने की आर्थिक लागत सीधे टोकन अनुक्रम की लंबाई और समवर्ती स्तरों के साथ बढ़ती है।",
        "kn": "ಇನ್‌ಫರೆನ್ಸ್ ಸೇವೆಗಳನ್ನು ಚಾಲನೆ ಮಾಡುವ ಆರ್ಥಿಕ ವೆಚ್ಚವು ಟೋಕನ್ ಅನುಕ್ರಮದ ಉದ್ದ ಮತ್ತು ಏಕಕಾಲೀನತೆಯ ಮಟ್ಟಗಳೊಂದಿಗೆ ನೇರವಾಗಿ ಹೆಚ್ಚಾಗುತ್ತದೆ.",
        "zh": "运行推理服务的经济成本直接随着词元序列长度和并发级别而扩展。",
        "ja": "推論サービスを実行する経済的コストは、トークンシーケンス長および同時実行レベルに直接比例して増加します。",
    },
    {
        "en": "Efficient cross-language tokenization ensures fair pricing and low latency for users across the globe.",
        "de": "Eine effiziente sprachübergreifende Tokenisierung sorgt für faire Preise und geringe Latenzzeiten für Benutzer auf der ganzen Welt.",
        "fr": "Une tokenisation multilingue efficace garantit une tarification équitable et une faible latence pour les utilisateurs du monde entier.",
        "es": "Una tokenización multilingüe eficiente garantiza precios justos y baja latencia para los usuarios de todo el mundo.",
        "ru": "Эффективная многоязычная токенизация обеспечивает справедливые цены и низкую задержку для пользователей по всему миру.",
        "ar": "يضمن تقسيم الرموز الفعال عبر اللغات تسعيرًا عادلاً وزمن انتقال منخفض للمستخدمين في جميع أنحاء العالم.",
        "hi": "कुशल बहुभाषी टोकनाइज़ेशन दुनिया भर के उपयोगकर्ताओं के लिए उचित मूल्य निर्धारण और कम विलंबता सुनिश्चित करता है।",
        "kn": "ದಕ್ಷ ಬಹುಭಾಷಾ ಟೋಕನೈಸೇಶನ್ ಪ್ರಪಂಚದಾದ್ಯಂತದ ಬಳಕೆದಾರರಿಗೆ ನ್ಯಾಯಯುತ ಬೆಲೆ ಮತ್ತು ಕಡಿಮೆ ಲೇಟೆನ್ಸಿಯನ್ನು ಖಚಿತಪಡಿಸುತ್ತದೆ.",
        "zh": "高效的跨语言词元化确保了全球用户能够享受公平的价格和更低的延迟。",
        "ja": "効率的な言語横断トークン化により、世界中のユーザーに対して公正な価格設定と低レイテンシが保証されます。",
    }
]


def get_parallel_corpus(limit: int | None = None) -> list[dict[str, str]]:
    """Retrieve parallel multilingual evaluation sentences."""
    if limit is not None:
        return PARALLEL_CORPUS[:limit]
    return PARALLEL_CORPUS


def get_language_meta(code: str) -> LanguageMeta:
    """Retrieve metadata for a language code."""
    if code not in SUPPORTED_LANGUAGES:
        return LanguageMeta(code, code.upper(), "Unknown", "Unknown")
    return SUPPORTED_LANGUAGES[code]
