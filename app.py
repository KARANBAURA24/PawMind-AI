from flask import Flask, request, render_template_string
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
@app.route("/")
def home():
    return "PawMind AI is live!"
# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {
    "png", "jpg", "jpeg", "gif", "webp",
    "mp4", "mov", "avi", "mkv", "webm"
}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def analyze_behavior(animal, behavior):
    """
    Basic local behavior analyzer.
    This works without an external AI API.
    """

    text = behavior.lower().strip()

    # Default response
    analysis = (
        f"The reported behavior of the {animal.lower()} "
        "should be considered in the context of its environment, "
        "routine, age, health and previous experiences."
    )

    possible_causes = [
        "Environmental changes",
        "Stress or anxiety",
        "Lack of stimulation or exercise",
        "Learned behavior",
        "Fear or uncertainty"
    ]

    training = [
        "Use calm and consistent interactions.",
        "Reward desirable behavior immediately.",
        "Avoid punishment or intimidation.",
        "Keep training sessions short and positive.",
        "Observe when and where the behavior happens."
    ]

    safety = (
        "If the behavior is sudden, severe, involves aggression, "
        "injury, unusual eating/drinking, or other signs of illness, "
        "contact a qualified veterinarian or animal behavior professional."
    )

    # -----------------------------------------------------
    # DOG
    # -----------------------------------------------------

    if animal == "Dog":

        if any(word in text for word in [
            "bark", "barking", "भौंक", "भौंकता"
        ]):
            analysis = (
                "The barking may be a form of communication. "
                "Dogs may bark because of excitement, alertness, fear, "
                "frustration, territorial behavior or a desire for attention."
            )

            possible_causes = [
                "Alerting to sounds or people",
                "Excitement",
                "Fear or anxiety",
                "Attention-seeking",
                "Insufficient physical or mental stimulation"
            ]

            training = [
                "Identify what triggers the barking.",
                "Reward calm behavior.",
                "Teach a calm or quiet cue using positive reinforcement.",
                "Provide appropriate exercise and mental enrichment.",
                "Avoid shouting, as this can increase arousal."
            ]

        elif any(word in text for word in [
            "bite", "biting", "aggressive", "aggression"
        ]):
            analysis = (
                "Biting or aggressive behavior can have several causes, "
                "including fear, pain, resource guarding, frustration or "
                "previous learning. The context and body language are important."
            )

            possible_causes = [
                "Fear or defensive behavior",
                "Pain or discomfort",
                "Resource guarding",
                "Frustration",
                "Previous learning or stressful experiences"
            ]

            training = [
                "Do not punish or physically confront the dog.",
                "Create distance from situations that trigger the behavior.",
                "Observe and record the circumstances surrounding the behavior.",
                "Use reward-based training with professional guidance.",
                "Seek veterinary or qualified behavior support if the behavior is concerning."
            ]

        elif any(word in text for word in [
            "chew", "chewing", "destroy", "destructive"
        ]):
            analysis = (
                "Destructive chewing can be normal exploratory behavior, "
                "especially in young dogs, but it can also be associated "
                "with boredom, stress or lack of appropriate outlets."
            )

            possible_causes = [
                "Exploration",
                "Teething",
                "Boredom",
                "Stress",
                "Insufficient enrichment"
            ]

            training = [
                "Provide appropriate chew toys.",
                "Reward the dog for choosing permitted objects.",
                "Increase age-appropriate enrichment.",
                "Keep valuable or unsafe objects out of reach.",
                "Maintain a predictable daily routine."
            ]

    # -----------------------------------------------------
    # CAT
    # -----------------------------------------------------

    elif animal == "Cat":

        if any(word in text for word in [
            "scratch", "scratching", "scratches"
        ]):
            analysis = (
                "Scratching is a normal feline behavior used for "
                "stretching, claw maintenance, communication and marking."
            )

            possible_causes = [
                "Normal claw maintenance",
                "Territorial marking",
                "Stretching",
                "Stress",
                "Preference for a particular surface"
            ]

            training = [
                "Provide a stable scratching post.",
                "Place scratching surfaces near preferred locations.",
                "Reward use of the scratching post.",
                "Protect furniture temporarily while redirecting behavior.",
                "Avoid punishment."
            ]

        elif any(word in text for word in [
            "hiss", "hissing", "aggressive", "aggression"
        ]):
            analysis = (
                "Hissing is commonly a warning signal that a cat is "
                "uncomfortable, frightened or wants more distance."
            )

            possible_causes = [
                "Fear",
                "Feeling threatened",
                "Pain or discomfort",
                "Territorial stress",
                "Overstimulation"
            ]

            training = [
                "Give the cat space.",
                "Avoid forcing interaction.",
                "Identify the situation that triggers the response.",
                "Provide safe hiding and resting areas.",
                "Use gradual, positive exposure when appropriate."
            ]

    # -----------------------------------------------------
    # HORSE
    # -----------------------------------------------------

    elif animal == "Horse":

        if any(word in text for word in [
            "kick", "kicking", "rear", "rearing"
        ]):
            analysis = (
                "Kicking or rearing can be associated with fear, pain, "
                "defensive behavior, frustration or learned responses. "
                "These behaviors deserve careful attention because horses "
                "are large and powerful animals."
            )

            possible_causes = [
                "Fear",
                "Pain or discomfort",
                "Frustration",
                "Defensive response",
                "Learned behavior"
            ]

            training = [
                "Prioritize handler and animal safety.",
                "Avoid escalating the situation.",
                "Check for possible physical discomfort.",
                "Use calm, consistent groundwork.",
                "Seek qualified professional help for dangerous behavior."
            ]

        elif any(word in text for word in [
            "spook", "spooking", "scared", "fear"
        ]):
            analysis = (
                "Spooking is often a response to something the horse "
                "perceives as unfamiliar, sudden or threatening."
            )

            possible_causes = [
                "Unfamiliar objects",
                "Sudden movement or sound",
                "Environmental changes",
                "Previous frightening experiences",
                "General anxiety"
            ]

            training = [
                "Introduce unfamiliar objects gradually.",
                "Keep sessions calm and predictable.",
                "Reward calm investigation.",
                "Avoid forcing the horse toward a frightening stimulus.",
                "Use qualified professional guidance when needed."
            ]

    # -----------------------------------------------------
    # BIRD
    # -----------------------------------------------------

    elif animal == "Bird":

        if any(word in text for word in [
            "scream", "screaming", "loud", "noise"
        ]):
            analysis = (
                "Loud vocalization can be normal bird communication, "
                "but unusually frequent or sudden changes may indicate "
                "attention-seeking, boredom, fear or environmental stress."
            )

            possible_causes = [
                "Communication",
                "Attention-seeking",
                "Boredom",
                "Fear",
                "Environmental stress"
            ]

            training = [
                "Maintain a predictable routine.",
                "Provide appropriate enrichment.",
                "Reward calm periods.",
                "Avoid reinforcing unwanted attention-seeking vocalization.",
                "Monitor sudden changes in behavior."
            ]

        elif any(word in text for word in [
            "feather", "plucking", "pluck"
        ]):
            analysis = (
                "Feather plucking can have behavioral, environmental or "
                "medical causes and should not automatically be treated "
                "as a training problem."
            )

            possible_causes = [
                "Stress",
                "Boredom",
                "Environmental problems",
                "Social factors",
                "Possible medical causes"
            ]

            training = [
                "Review enrichment and daily routine.",
                "Provide appropriate opportunities for natural behaviors.",
                "Reduce unnecessary environmental stress.",
                "Monitor how frequently the behavior occurs.",
                "Consult an avian veterinarian if the behavior persists."
            ]

    # -----------------------------------------------------
    # RABBIT
    # -----------------------------------------------------

    elif animal == "Rabbit":

        if any(word in text for word in [
            "bite", "biting", "aggressive", "aggression"
        ]):
            analysis = (
                "A rabbit may bite when frightened, stressed, territorial, "
                "overhandled or uncomfortable. Body language and context "
                "are important for understanding the cause."
            )

            possible_causes = [
                "Fear",
                "Territorial behavior",
                "Stress",
                "Overhandling",
                "Pain or discomfort"
            ]

            training = [
                "Approach calmly and predictably.",
                "Allow the rabbit to retreat to a safe area.",
                "Avoid forcing physical interaction.",
                "Reward calm interactions.",
                "Consider veterinary advice if the behavior is sudden."
            ]

        elif any(word in text for word in [
            "thump", "thumping", "stomp"
        ]):
            analysis = (
                "Foot thumping is a natural rabbit warning signal and "
                "can indicate fear, alarm or concern about something nearby."
            )

            possible_causes = [
                "Fear",
                "Unexpected sounds",
                "Perceived danger",
                "Environmental stress",
                "Unfamiliar surroundings"
            ]

            training = [
                "Identify possible environmental triggers.",
                "Provide a secure hiding area.",
                "Keep the environment predictable.",
                "Avoid sudden handling.",
                "Monitor whether the behavior is becoming more frequent."
            ]

    return analysis, possible_causes, training, safety


# ---------------------------------------------------------
# HTML PAGE
# ---------------------------------------------------------

HTML = """
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>PawMind AI | Animal Behavior Assistant</title>

    <style>

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family:
                Inter,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;

            background: #f4f8f6;
            color: #18352e;
            line-height: 1.6;
        }

        /* ---------------------------------------------
           HERO
        --------------------------------------------- */

        .hero {
            background:
                linear-gradient(
                    135deg,
                    #11745f,
                    #21876f,
                    #177761
                );

            color: white;
            padding: 65px 8% 75px;

            position: relative;
            overflow: hidden;
        }

        .hero::before {
            content: "";
            position: absolute;
            width: 400px;
            height: 400px;
            border-radius: 50%;
            background: rgba(255,255,255,0.05);
            right: -120px;
            top: -180px;
        }

        .hero-content {
            max-width: 1250px;
            margin: auto;
            position: relative;
            z-index: 2;
        }

        .badge {
            display: inline-block;
            background: rgba(255,255,255,0.14);
            border: 1px solid rgba(255,255,255,0.12);
            padding: 10px 20px;
            border-radius: 30px;
            font-weight: 600;
            margin-bottom: 22px;
            backdrop-filter: blur(10px);
        }

        .hero h1 {
            font-size: clamp(42px, 5vw, 68px);
            line-height: 1.05;
            max-width: 760px;
            letter-spacing: -2px;
            margin-bottom: 25px;
        }

        .hero p {
            max-width: 780px;
            font-size: 19px;
            color: rgba(255,255,255,0.9);
        }

        .hero-animal {
            position: absolute;
            right: 9%;
            bottom: 35px;
            font-size: 95px;
            animation: floatAnimal 3s ease-in-out infinite;
        }

        @keyframes floatAnimal {
            0%,100% {
                transform: translateY(0);
            }

            50% {
                transform: translateY(-12px);
            }
        }

        /* ---------------------------------------------
           MAIN
        --------------------------------------------- */

        .container {
            max-width: 1250px;
            margin: auto;
            padding: 55px 25px 80px;
        }

        .section-title {
            margin-bottom: 25px;
        }

        .section-title h2 {
            font-size: 32px;
            margin-bottom: 5px;
        }

        .section-title p {
            color: #698078;
            font-size: 16px;
        }

        /* ---------------------------------------------
           ANIMAL CARDS
        --------------------------------------------- */

        .animals {
            display: grid;
            grid-template-columns:
                repeat(5, minmax(0, 1fr));

            gap: 18px;
            margin-bottom: 45px;
        }

        .animal-card {
            background: white;
            min-height: 150px;
            border-radius: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;

            border: 2px solid transparent;

            box-shadow:
                0 8px 25px rgba(28,65,56,0.06);

            cursor: pointer;

            transition:
                transform 0.25s ease,
                box-shadow 0.25s ease,
                border-color 0.25s ease,
                background 0.25s ease;
        }

        .animal-card:hover {
            transform: translateY(-7px);

            box-shadow:
                0 18px 35px rgba(28,65,56,0.12);

            border-color: #3aa486;
        }

        .animal-card.selected {
            border-color: #13856c;
            background: #ecfaf5;
            transform: translateY(-5px);
        }

        .animal-icon {
            font-size: 52px;
            margin-bottom: 8px;
        }

        .animal-card strong {
            font-size: 17px;
        }

        /* ---------------------------------------------
           ANALYSIS BOX
        --------------------------------------------- */

        .analysis-box {
            background: white;
            border-radius: 28px;
            padding: 40px;

            box-shadow:
                0 15px 50px rgba(27,66,57,0.08);

            margin-bottom: 40px;
        }

        .analysis-heading {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 8px;
        }

        .analysis-heading h2 {
            font-size: 29px;
        }

        .analysis-heading span {
            font-size: 30px;
        }

        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
            margin-top: 30px;
        }

        .field {
            display: flex;
            flex-direction: column;
        }

        .field.full {
            grid-column: 1 / -1;
        }

        label {
            font-weight: 700;
            margin-bottom: 9px;
            color: #21483e;
        }

        select,
        input[type="file"],
        textarea {
            width: 100%;
            border: 1px solid #d8e4df;
            border-radius: 13px;
            background: #fbfdfc;
            padding: 14px 15px;
            font-size: 15px;
            color: #18352e;
            outline: none;

            transition:
                border-color .2s,
                box-shadow .2s;
        }

        select:focus,
        input[type="file"]:focus,
        textarea:focus {
            border-color: #269b7c;

            box-shadow:
                0 0 0 4px rgba(38,155,124,0.10);
        }

        textarea {
            min-height: 160px;
            resize: vertical;
            font-family: inherit;
        }

        .upload-box {
            padding: 5px 0;
        }

        .file-note {
            margin-top: 8px;
            color: #758982;
            font-size: 13px;
        }

        .analyze-btn {
            margin-top: 28px;
            border: none;
            border-radius: 14px;

            background:
                linear-gradient(
                    135deg,
                    #117b63,
                    #21a27f
                );

            color: white;
            padding: 16px 28px;

            font-size: 17px;
            font-weight: 700;

            cursor: pointer;

            box-shadow:
                0 10px 22px rgba(17,123,99,0.22);

            transition:
                transform .2s,
                box-shadow .2s;
        }

        .analyze-btn:hover {
            transform: translateY(-3px);

            box-shadow:
                0 14px 28px rgba(17,123,99,0.30);
        }

        /* ---------------------------------------------
           RESULT
        --------------------------------------------- */

        .result {
            margin-top: 35px;
            background: #f6fbf9;
            border: 1px solid #d9ebe5;
            border-radius: 20px;
            padding: 30px;
        }

        .result h3 {
            font-size: 23px;
            margin-bottom: 20px;
            color: #126d59;
        }

        .result p {
            margin-bottom: 17px;
        }

        .result strong {
            color: #174d41;
        }

        .result-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 25px;
        }

        .result-card {
            background: white;
            border-radius: 17px;
            padding: 23px;

            border: 1px solid #e0ece8;
        }

        .result-card h4 {
            margin-bottom: 14px;
            font-size: 18px;
        }

        .result-card ul {
            padding-left: 20px;
        }

        .result-card li {
            margin-bottom: 8px;
        }

        .safety {
            margin-top: 20px;
            padding: 17px 20px;
            background: #fff8e9;
            border: 1px solid #f2dfb1;
            border-radius: 13px;
            color: #654e1b;
        }

        /* ---------------------------------------------
           FEATURES
        --------------------------------------------- */

        .features {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 22px;
            margin-top: 40px;
        }

        .feature {
            background: white;
            border-radius: 20px;
            padding: 28px;

            box-shadow:
                0 8px 25px rgba(28,65,56,0.05);
        }

        .feature-icon {
            font-size: 35px;
            margin-bottom: 12px;
        }

        .feature h3 {
            margin-bottom: 7px;
            font-size: 20px;
        }

        .feature p {
            color: #71827d;
        }

        /* ---------------------------------------------
           FOOTER
        --------------------------------------------- */

        footer {
            text-align: center;
            padding: 30px 20px;
            color: #758680;
            border-top: 1px solid #e1ebe7;
            background: white;
        }

        /* ---------------------------------------------
           RESPONSIVE
        --------------------------------------------- */

        @media (max-width: 950px) {

            .animals {
                grid-template-columns:
                    repeat(3, 1fr);
            }

            .hero-animal {
                display: none;
            }

            .form-grid {
                grid-template-columns: 1fr;
            }

            .field.full {
                grid-column: auto;
            }

            .result-grid {
                grid-template-columns: 1fr;
            }

            .features {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 600px) {

            .hero {
                padding: 45px 25px 55px;
            }

            .hero h1 {
                font-size: 42px;
            }

            .container {
                padding: 40px 18px;
            }

            .animals {
                grid-template-columns:
                    repeat(2, 1fr);
            }

            .analysis-box {
                padding: 25px 20px;
            }

        }

    </style>

</head>


<body>

    <!-- =================================================
         HERO
    ================================================== -->

    <section class="hero">

        <div class="hero-content">

            <div class="badge">
                ✨ AI-Powered Animal Behavior Assistant
            </div>

            <h1>
                Understand Your Animal Better.
            </h1>

            <p>
                Analyze animal behavior, understand possible causes,
                and discover responsible training recommendations
                with PawMind AI.
            </p>

        </div>

        <div class="hero-animal">
            🐕
        </div>

    </section>


    <!-- =================================================
         MAIN
    ================================================== -->

    <main class="container">


        <!-- ANIMAL SELECTION -->

        <div class="section-title">

            <h2>
                Choose an Animal
            </h2>

            <p>
                Select the animal you want to analyze.
            </p>

        </div>


        <div class="animals">

            <div
                class="animal-card"
                data-animal="Dog"
                onclick="selectAnimal('Dog', this)"
            >

                <div class="animal-icon">
                    🐕
                </div>

                <strong>
                    Dog
                </strong>

            </div>


            <div
                class="animal-card"
                data-animal="Cat"
                onclick="selectAnimal('Cat', this)"
            >

                <div class="animal-icon">
                    🐈
                </div>

                <strong>
                    Cat
                </strong>

            </div>


            <div
                class="animal-card"
                data-animal="Horse"
                onclick="selectAnimal('Horse', this)"
            >

                <div class="animal-icon">
                    🐎
                </div>

                <strong>
                    Horse
                </strong>

            </div>


            <div
                class="animal-card"
                data-animal="Bird"
                onclick="selectAnimal('Bird', this)"
            >

                <div class="animal-icon">
                    🦜
                </div>

                <strong>
                    Bird
                </strong>

            </div>


            <div
                class="animal-card"
                data-animal="Rabbit"
                onclick="selectAnimal('Rabbit', this)"
            >

                <div class="animal-icon">
                    🐇
                </div>

                <strong>
                    Rabbit
                </strong>

            </div>

        </div>


        <!-- =================================================
             ANALYSIS FORM
        ================================================== -->

        <section
            id="analysis"
            class="analysis-box"
        >

            <div class="analysis-heading">

                <span>
                    🔍
                </span>

                <h2>
                    Behavior Analysis
                </h2>

            </div>

            <p style="color:#71827d;">
                Tell us what you have observed.
            </p>


            <form
                method="POST"
                enctype="multipart/form-data"
            >

                <div class="form-grid">


                    <!-- ANIMAL -->

                    <div class="field">

                        <label>
                            Select Animal
                        </label>

                        <select
                            id="animalSelect"
                            name="animal"
                            required
                        >

                            <option value="">
                                Choose animal...
                            </option>

                            <option value="Dog">
                                🐕 Dog
                            </option>

                            <option value="Cat">
                                🐈 Cat
                            </option>

                            <option value="Horse">
                                🐎 Horse
                            </option>

                            <option value="Bird">
                                🦜 Bird
                            </option>

                            <option value="Rabbit">
                                🐇 Rabbit
                            </option>

                        </select>

                    </div>


                    <!-- FILE -->

                    <div class="field">

                        <label>
                            Upload Photo / Video
                        </label>

                        <div class="upload-box">

                            <input
                                type="file"
                                name="media"
                                accept="image/*,video/*"
                            >

                            <div class="file-note">
                                Optional — JPG, PNG, MP4, MOV, WEBM and more.
                            </div>

                        </div>

                    </div>


                    <!-- BEHAVIOR -->

                    <div class="field full">

                        <label>
                            Describe the Behavior
                        </label>

                        <textarea
                            name="behavior"
                            placeholder="Example: My dog starts barking and becomes restless whenever someone approaches the house."
                            required
                        ></textarea>

                    </div>

                </div>


                <button
                    class="analyze-btn"
                    type="submit"
                >
                    🧠 Analyze Behavior
                </button>

            </form>


            {% if result %}

            <!-- =================================================
                 RESULT
            ================================================== -->

            <div class="result">

                <h3>
                    📊 Initial Analysis
                </h3>


                <p>
                    <strong>
                        Animal:
                    </strong>

                    {{ animal }}
                </p>


                <p>
                    <strong>
                        Observed behavior:
                    </strong>

                    {{ behavior }}
                </p>


                <p>
                    <strong>
                        AI Behavior Analysis:
                    </strong>
                    <br>

                    {{ result }}
                </p>


                <div class="result-grid">


                    <!-- POSSIBLE CAUSES -->

                    <div class="result-card">

                        <h4>
                            🔎 Possible Causes
                        </h4>

                        <ul>

                            {% for cause in causes %}

                            <li>
                                {{ cause }}
                            </li>

                            {% endfor %}

                        </ul>

                    </div>


                    <!-- TRAINING -->

                    <div class="result-card">

                        <h4>
                            🎯 Training Guidance
                        </h4>

                        <ul>

                            {% for item in training %}

                            <li>
                                {{ item }}
                            </li>

                            {% endfor %}

                        </ul>

                    </div>

                </div>


                <div class="safety">

                    <strong>
                        ⚠️ Important:
                    </strong>

                    {{ safety }}

                </div>

            </div>

            {% endif %}

        </section>


        <!-- =================================================
             FEATURES
        ================================================== -->

        <div
            id="features"
            class="features"
        >


            <div class="feature">

                <div class="feature-icon">
                    🧠
                </div>

                <h3>
                    AI Behavior Analysis
                </h3>

                <p>
                    Analyze reported behaviors and identify
                    possible behavioral patterns.
                </p>

            </div>


            <div class="feature">

                <div class="feature-icon">
                    🎯
                </div>

                <h3>
                    Training Guidance
                </h3>

                <p>
                    Get practical, humane and responsible
                    training suggestions.
                </p>

            </div>


            <div class="feature">

                <div class="feature-icon">
                    🛡️
                </div>

                <h3>
                    Responsible Approach
                </h3>

                <p>
                    Understand behavior without relying on
                    punishment or intimidation.
                </p>

            </div>


        </div>

    </main>


    <!-- =================================================
         FOOTER
    ================================================== -->

    <footer>

        <p>
            🐾 PawMind AI — Animal Behavior Assistant
        </p>

        <p style="font-size:13px; margin-top:5px;">
            For educational guidance. Not a substitute for
            veterinary or professional behavioral care.
        </p>

    </footer>


    <!-- =================================================
         JAVASCRIPT
    ================================================== -->

    <script>

        function selectAnimal(animal, card) {

            // Select animal in dropdown
            const dropdown =
                document.getElementById("animalSelect");

            dropdown.value = animal;


            // Remove selected class from every card
            const cards =
                document.querySelectorAll(".animal-card");

            cards.forEach(function(item) {

                item.classList.remove("selected");

            });


            // Highlight clicked card
            card.classList.add("selected");


            // Scroll to analysis form
            document.getElementById("analysis")
                .scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

        }


        // If dropdown is changed manually,
        // highlight corresponding card.

        document
            .getElementById("animalSelect")
            .addEventListener("change", function() {

                const selectedAnimal = this.value;

                const cards =
                    document.querySelectorAll(".animal-card");

                cards.forEach(function(card) {

                    if (
                        card.dataset.animal === selectedAnimal
                    ) {

                        card.classList.add("selected");

                    } else {

                        card.classList.remove("selected");

                    }

                });

            });

    </script>


</body>

</html>
"""


# ---------------------------------------------------------
# FLASK ROUTE
# ---------------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    animal = ""
    behavior = ""
    causes = []
    training = []
    safety = ""

    if request.method == "POST":

        animal = request.form.get("animal", "").strip()
        behavior = request.form.get("behavior", "").strip()

        # ---------------------------------------------
        # VALIDATION
        # ---------------------------------------------

        if not animal:
            return render_template_string(
                HTML,
                result="Please select an animal.",
                animal=animal,
                behavior=behavior,
                causes=[],
                training=[],
                safety=""
            )

        if not behavior:
            return render_template_string(
                HTML,
                result="Please describe the observed behavior.",
                animal=animal,
                behavior=behavior,
                causes=[],
                training=[],
                safety=""
            )

        # ---------------------------------------------
        # FILE UPLOAD
        # ---------------------------------------------

        media = request.files.get("media")

        if media and media.filename:

            if allowed_file(media.filename):

                filename = secure_filename(media.filename)

                filepath = os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )

                media.save(filepath)

            else:

                return render_template_string(
                    HTML,
                    result="The uploaded file type is not supported.",
                    animal=animal,
                    behavior=behavior,
                    causes=[],
                    training=[],
                    safety=""
                )

        # ---------------------------------------------
        # ANALYSIS
        # ---------------------------------------------

        (
            result,
            causes,
            training,
            safety
        ) = analyze_behavior(
            animal,
            behavior
        )

    return render_template_string(
        HTML,
        result=result,
        animal=animal,
        behavior=behavior,
        causes=causes,
        training=training,
        safety=safety
    )


# ---------------------------------------------------------
# RUN APPLICATION
# ---------------------------------------------------------

if __name__ == "__main__":

  app.run(
    host="0.0.0.0",
    port=5000,
    debug=True
)
