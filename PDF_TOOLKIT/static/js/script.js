const aiForm = document.getElementById("aiChatForm");
let currentDocumentId = null;


// ========================================
// ELEMENTS
// ========================================

const processPdfBtn =
    document.getElementById("processPdfBtn");

const askAiBtn =
    document.getElementById("askAiBtn");

const aiPdfFile =
    document.getElementById("aiPdfFile");

const aiStatus =
    document.getElementById("aiStatus");

const aiChatSection =
    document.getElementById("aiChatSection");

const aiQuestion =
    document.getElementById("aiQuestion");

const aiAnswer =
    document.getElementById("aiAnswer");

const aiLoading =
    document.getElementById("aiLoading");


// ========================================
// PROCESS PDF
// ========================================

if (processPdfBtn) {

    processPdfBtn.addEventListener(
        "click",
        async function () {

            const file =
                aiPdfFile.files[0];


            if (!file) {

                aiStatus.textContent =
                    "Please select a PDF.";

                return;
            }


            const formData =
                new FormData();


            formData.append(
                "file",
                file
            );


            aiStatus.textContent =
                "Processing PDF and creating embeddings...";


            processPdfBtn.disabled = true;


            try {

                const response =
                    await fetch(
                        "/ai-upload",
                        {
                            method: "POST",
                            body: formData
                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    aiStatus.textContent =
                        "Error: " +
                        data.error;

                    return;
                }


                currentDocumentId =
                    data.document_id;


                aiStatus.textContent =
                    "PDF ready! You can now ask questions.";


                aiChatSection.style.display =
                    "block";


            }

            catch (error) {

                console.error(error);

                aiStatus.textContent =
                    "Unable to process PDF.";

            }

            finally {

                processPdfBtn.disabled =
                    false;

            }

        }
    );
}

// ========================================
// ASK QUESTION
// ========================================

if (askAiBtn) {

    askAiBtn.addEventListener(
        "click",
        async function () {

            const question =
                aiQuestion.value.trim();


            if (!currentDocumentId) {

                aiAnswer.textContent =
                    "Process a PDF first.";

                return;
            }


            if (!question) {

                aiAnswer.textContent =
                    "Please enter a question.";

                return;
            }


            aiLoading.style.display =
                "block";


            aiAnswer.textContent = "";

            askAiBtn.disabled = true;


            try {

                const response =
                    await fetch(
                        "/ai-question",
                        {

                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({

                                document_id:
                                    currentDocumentId,

                                question:
                                    question

                            })

                        }
                    );


                const data =
                    await response.json();


                if (!response.ok) {

                    aiAnswer.textContent =
                        "Error: " +
                        data.error;

                    return;
                }


                let result =
                    data.answer;


                if (
                    data.pages &&
                    data.pages.length > 0
                ) {

                    result +=
                        "\n\nRelevant pages: " +
                        data.pages.join(", ");

                }


                aiAnswer.textContent =
                    result;


            }

            catch (error) {

                console.error(error);

                aiAnswer.textContent =
                    "Unable to get AI response.";

            }

            finally {

                aiLoading.style.display =
                    "none";

                askAiBtn.disabled =
                    false;

            }

        }
    );
}