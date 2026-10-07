const API_URL = "http://127.0.0.1:8000";

const searchInput = document.getElementById("searchInput");
const policyList = document.getElementById("policyList");
const status = document.getElementById("status");

const discussionInput = document.getElementById("discussionInput");
const analyzeButton = document.getElementById("analyzeButton");
const analysisStatus = document.getElementById("analysisStatus");

const analysisResult = document.getElementById("analysisResult");


// Store policies
let policies = [];


// ------------------------------------
// LOAD POLICIES
// ------------------------------------

async function loadPolicies() {

    try {

        status.textContent = "Loading policies...";

        const response = await fetch(`${API_URL}/policies`);

        if (!response.ok) {
            throw new Error("Failed to fetch policies");
        }

        policies = await response.json();

        status.textContent = `${policies.length} policies found`;

        displayPolicies(policies);

    } catch (error) {

        console.error(error);

        status.textContent =
            "Unable to connect to PolicyPulse API.";

    }
}


// ------------------------------------
// DISPLAY POLICIES
// ------------------------------------

function displayPolicies(policyData) {

    policyList.innerHTML = "";

    policyData.forEach(policy => {

        const card = document.createElement("div");

        card.className = "policy-card";

        card.innerHTML = `
            <h3>${policy.policy_name}</h3>

            <p>
                <strong>Sector:</strong>
                ${policy.sector}
            </p>

            <p>
                ${policy.description}
            </p>

            <p>
                <strong>Launch Date:</strong>
                ${policy.launch_date}
            </p>

            <a
                href="${policy.official_url}"
                target="_blank"
            >
                Official Website →
            </a>
        `;

        policyList.appendChild(card);

    });
}


// ------------------------------------
// SEARCH POLICIES
// ------------------------------------

searchInput.addEventListener("input", function () {

    const query = searchInput.value.toLowerCase().trim();

    const filteredPolicies = policies.filter(policy => {

        return (
            policy.policy_name.toLowerCase().includes(query) ||
            policy.sector.toLowerCase().includes(query) ||
            policy.description.toLowerCase().includes(query)
        );

    });

    displayPolicies(filteredPolicies);

    status.textContent =
        `${filteredPolicies.length} policies found`;
});


// ------------------------------------
// ANALYZE DISCUSSION
// ------------------------------------

analyzeButton.addEventListener("click", analyzeDiscussion);


async function analyzeDiscussion() {

    const text = discussionInput.value.trim();

    if (!text) {

        analysisStatus.textContent =
            "Please enter a discussion first.";

        analysisResult.classList.add("hidden");

        return;
    }


    try {

        analyzeButton.disabled = true;

        analyzeButton.textContent = "Analyzing...";

        analysisStatus.textContent = "";


        const response = await fetch(`${API_URL}/analyze`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                text: text
            })

        });


        if (!response.ok) {

            const errorData = await response.json();

            throw new Error(
                errorData.detail || "Analysis failed"
            );

        }


        const result = await response.json();


        // Show result
        analysisResult.classList.remove("hidden");


        // Stance
        document.getElementById("stance").textContent =
            result.stance;


        // Confidence
        document.getElementById("confidence").textContent =
            `${(result.confidence * 100).toFixed(2)}%`;


        // Probabilities
        updateProbability(
            "supportive",
            result.probabilities.supportive
        );

        updateProbability(
            "opposed",
            result.probabilities.opposed
        );

        updateProbability(
            "neutral",
            result.probabilities.neutral
        );

        updateProbability(
            "mixed",
            result.probabilities.mixed
        );


    } catch (error) {

        console.error(error);

        analysisStatus.textContent =
            `Error: ${error.message}`;

        analysisResult.classList.add("hidden");

    } finally {

        analyzeButton.disabled = false;

        analyzeButton.textContent =
            "Analyze Discussion";
    }
}


// ------------------------------------
// UPDATE PROBABILITY BAR
// ------------------------------------

function updateProbability(label, probability) {

    const percentage =
        probability * 100;


    document.getElementById(
        `${label}Value`
    ).textContent =
        `${percentage.toFixed(2)}%`;


    document.getElementById(
        `${label}Bar`
    ).style.width =
        `${percentage}%`;
}
// ------------------------------------
// LOAD ANALYTICS
// ------------------------------------

async function loadAnalytics() {

    try {

        const response = await fetch(`${API_URL}/analytics`);

        if (!response.ok) {
            throw new Error("Failed to load analytics");
        }

        const data = await response.json();

        document.getElementById("totalDiscussions").textContent =
            data.total_discussions;

        document.getElementById("supportiveCount").textContent =
            `${data.stance_percentages.supportive || 0}%`;

        document.getElementById("opposedCount").textContent =
            `${data.stance_percentages.opposed || 0}%`;

        document.getElementById("neutralCount").textContent =
            `${data.stance_percentages.neutral || 0}%`;

        document.getElementById("mixedCount").textContent =
            `${data.stance_percentages.mixed || 0}%`;

    } catch (error) {

        console.error("Analytics error:", error);

    }
}

// ------------------------------------
// INITIAL LOAD
// ------------------------------------

loadPolicies();
loadAnalytics();