(() => {
    "use strict";


    /* =========================
       DOM
       ========================= */

    const questionInput =
        document.getElementById("questionInput");

    const sendButton =
        document.getElementById("sendButton");

    const welcomeView =
        document.getElementById("welcomeView");

    const chatView =
        document.getElementById("chatView");

    const chatMessages =
        document.getElementById("chatMessages");

    const chatScrollArea =
        document.getElementById("chatScrollArea");

    const errorMessage =
        document.getElementById("errorMessage");

    const newChatButton =
        document.getElementById("newChatButton");

    const suggestionButtons =
        document.querySelectorAll(".suggestion-question");


    /* =========================
       Custom Program Dropdown
       ========================= */

    const programDropdownWrapper =
        document.getElementById("programDropdownWrapper");

    const programDropdownButton =
        document.getElementById("programDropdownButton");

    const programDropdownMenu =
        document.getElementById("programDropdownMenu");

    const programDropdownLabel =
        document.getElementById("programDropdownLabel");

    const programOptions =
        document.querySelectorAll(".program-option");


    /* =========================
       State
       ========================= */

    let isLoading = false;

    let selectedProgram = "";


    /* =========================
       Suggestion Questions
       ========================= */

    suggestionButtons.forEach((button) => {

        button.addEventListener("click", () => {

            questionInput.value =
                button.dataset.question ?? "";

            questionInput.focus();

            autoResizeTextarea();

            updateSendState();

        });

    });


    /* =========================
       Custom Dropdown
       ========================= */

    programDropdownButton.addEventListener(
        "click",
        (event) => {

            event.stopPropagation();

            programDropdownMenu.classList.toggle(
                "hidden"
            );


            const isOpen =
                !programDropdownMenu.classList.contains(
                    "hidden"
                );


            programDropdownButton.setAttribute(
                "aria-expanded",
                String(isOpen)
            );

        }
    );


    /* เลือกสาขา */

    programOptions.forEach((option) => {

        option.addEventListener("click", () => {

            /*
                data-value จะเป็น:
                IT
                AI
                BIT
                DSBA
            */

            selectedProgram =
                option.dataset.value ?? "";


            /*
                ข้อความที่แสดง เช่น
                AIT

                แต่ค่าที่ส่ง backend ยังเป็น AI
            */

            programDropdownLabel.textContent =
                option.textContent.trim();


            programDropdownMenu.classList.add(
                "hidden"
            );


            programDropdownButton.setAttribute(
                "aria-expanded",
                "false"
            );


            clearError();

            updateSendState();

        });

    });


    /* กดพื้นที่ข้างนอก dropdown */

    document.addEventListener(
        "click",
        (event) => {

            if (
                programDropdownWrapper &&
                !programDropdownWrapper.contains(
                    event.target
                )
            ) {

                programDropdownMenu.classList.add(
                    "hidden"
                );


                programDropdownButton.setAttribute(
                    "aria-expanded",
                    "false"
                );

            }

        }
    );


    /* =========================
       New Chat
       ========================= */

    newChatButton.addEventListener(
        "click",
        () => {

            /*
                ล้างข้อความเก่า
            */

            chatMessages.textContent = "";


            /*
                ล้างคำถาม
            */

            questionInput.value = "";

            autoResizeTextarea();


            /*
                Reset สาขา
            */

            selectedProgram = "";

            programDropdownLabel.textContent =
                "เลือกสาขา";

            programDropdownMenu.classList.add(
                "hidden"
            );

            programDropdownButton.setAttribute(
                "aria-expanded",
                "false"
            );


            /*
                กลับหน้าแรก
            */

            chatView.classList.add(
                "hidden"
            );

            welcomeView.classList.remove(
                "hidden"
            );


            clearError();

            updateSendState();

            questionInput.focus();

        }
    );


    /* =========================
       Send Button State
       ========================= */

    function updateSendState() {

        const hasQuestion =
            questionInput.value
                .trim()
                .length >= 2;


        const hasProgram =
            selectedProgram !== "";


        const canSend =
            hasQuestion &&
            hasProgram &&
            !isLoading;


        sendButton.disabled =
            !canSend;


        /*
            JavaScript เปลี่ยน State/Class
            CSS เป็นคนกำหนดสี
        */

        sendButton.classList.toggle(
            "active",
            canSend
        );


        sendButton.classList.toggle(
            "disabled",
            !canSend
        );

    }


    /* =========================
       Question Input
       ========================= */

    questionInput.addEventListener(
        "input",
        () => {

            autoResizeTextarea();

            clearError();

            updateSendState();

        }
    );


    /* =========================
       Auto Resize Textarea
       ========================= */

    function autoResizeTextarea() {

        questionInput.style.height =
            "auto";


        questionInput.style.height =
            Math.min(
                questionInput.scrollHeight,
                160
            ) + "px";

    }


    /* =========================
       Error
       ========================= */

    function showError(message) {

        errorMessage.textContent =
            message;

        errorMessage.classList.remove(
            "hidden"
        );

    }


    function clearError() {

        errorMessage.textContent =
            "";

        errorMessage.classList.add(
            "hidden"
        );

    }


    /* =========================
       User Message
       ========================= */

    function addUserMessage(
        question,
        program
    ) {

        const row =
            document.createElement("div");


        row.className =
            "flex justify-end";


        const bubble =
            document.createElement("div");


        bubble.className =
            "user-message";


        /* Program label */

        const programLabel =
            document.createElement("div");


        programLabel.className =
            "text-xs text-blue-600 mb-2";


        /*
            ถ้า backend ใช้ AI
            แต่เราอยากโชว์ AIT
        */

        programLabel.textContent =
            program === "AI"
                ? "AIT"
                : program;


        /* Question */

        const questionText =
            document.createElement("div");


        questionText.textContent =
            question;


        bubble.appendChild(
            programLabel
        );

        bubble.appendChild(
            questionText
        );

        row.appendChild(
            bubble
        );

        chatMessages.appendChild(
            row
        );

    }


    /* =========================
       Assistant Message
       ========================= */

    function addAssistantMessage(answer) {

        const row =
            document.createElement("div");


        row.className =
            "flex justify-start";


        const bubble =
            document.createElement("div");


        bubble.className =
            "assistant-message";


        /*
            ใช้ textContent
            ไม่ใช้ innerHTML
        */

        bubble.textContent =
            answer;


        row.appendChild(
            bubble
        );

        chatMessages.appendChild(
            row
        );

    }


    /* =========================
       Loading
       ========================= */

    function addLoadingMessage() {

        const row =
            document.createElement("div");


        row.className =
            "flex justify-start";


        const loading =
            document.createElement("div");


        loading.className =
            "loading-message";


        /* Spinner */

        const spinner =
            document.createElement("span");


        spinner.className =
            "loading-spinner";


        /* Text */

        const text =
            document.createElement("span");


        text.textContent =
            "กำลังค้นหาข้อมูล...";


        loading.appendChild(
            spinner
        );

        loading.appendChild(
            text
        );

        row.appendChild(
            loading
        );

        chatMessages.appendChild(
            row
        );


        return row;

    }


    /* =========================
       POST /api/ask
       ========================= */

    async function sendQuestion() {

        clearError();


        const question =
            questionInput.value.trim();


        /*
            ตรงนี้ใช้ Custom Dropdown แล้ว
        */

        const program =
            selectedProgram;


        /* =====================
           Frontend Validation
           ===================== */

        if (question.length < 2) {

            showError(
                "กรุณาพิมพ์คำถาม"
            );

            return;

        }


        if (!program) {

            showError(
                "กรุณาเลือกสาขาก่อนส่งคำถาม"
            );

            return;

        }


        if (isLoading) {
            return;
        }


        /* =====================
           Loading State
           ===================== */

        isLoading = true;

        updateSendState();


        /*
            จากหน้า Welcome
            -> หน้า Chat
        */

        welcomeView.classList.add(
            "hidden"
        );

        chatView.classList.remove(
            "hidden"
        );


        /*
            แสดงคำถามฝั่งขวา
        */

        addUserMessage(
            question,
            program
        );


        /*
            ล้างช่องคำถาม
        */

        questionInput.value = "";

        autoResizeTextarea();


        /*
            Loading ฝั่งซ้าย
        */

        const loadingMessage =
            addLoadingMessage();


        scrollToBottom();


        try {

            /*
                Frontend เรียก Backend

                ไม่มี API Key
                อยู่ใน JavaScript
            */

            const response =
                await fetch(
                    "/api/ask",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({
                                program:
                                    program,

                                question:
                                    question
                            })
                    }
                );


            /*
                แปลง Response เป็น JSON
            */

            let data;


            try {

                data =
                    await response.json();

            } catch {

                throw new Error(
                    "Server ส่งข้อมูลกลับมาไม่ถูกต้อง"
                );

            }


            /*
                fetch เจอ 400 / 404 / 500
                จะไม่เข้า catch เอง

                จึงต้องเช็ก response.ok
            */

            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    `HTTP ${response.status}`
                );

            }


            /*
                เอา Loading ออก
            */

            loadingMessage.remove();


            /* =====================
               Success State
               ===================== */

            addAssistantMessage(
                data.answer ||
                "ไม่พบคำตอบ"
            );


        } catch (error) {

            loadingMessage.remove();


            /* =====================
               Error State
               ===================== */

            const message =
                error instanceof Error
                    ? error.message
                    : "เกิดข้อผิดพลาด";


            showError(
                message
            );


            addAssistantMessage(
                "ไม่สามารถประมวลผลคำถามได้ กรุณาลองใหม่อีกครั้ง"
            );


        } finally {

            isLoading =
                false;


            updateSendState();


            questionInput.focus();


            scrollToBottom();

        }

    }


    /* =========================
       Send Button
       ========================= */

    sendButton.addEventListener(
        "click",
        sendQuestion
    );


    /* =========================
       Keyboard

       Enter = ส่ง
       Shift + Enter = ขึ้นบรรทัดใหม่
       ========================= */

    questionInput.addEventListener(
        "keydown",
        (event) => {

            if (
                event.key === "Enter" &&
                !event.shiftKey
            ) {

                event.preventDefault();


                if (
                    !sendButton.disabled
                ) {

                    sendQuestion();

                }

            }

        }
    );


    /* =========================
       Scroll Chat
       ========================= */

    function scrollToBottom() {

        requestAnimationFrame(
            () => {

                chatScrollArea.scrollTo({
                    top:
                        chatScrollArea.scrollHeight,

                    behavior:
                        "smooth"
                });

            }
        );

    }


    /* =========================
       Initial State
       ========================= */

    programDropdownMenu.classList.add(
        "hidden"
    );

    programDropdownButton.setAttribute(
        "aria-expanded",
        "false"
    );

    updateSendState();

})();