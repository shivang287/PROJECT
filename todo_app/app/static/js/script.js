document.addEventListener("DOMContentLoaded", () => {

    /*
     * =====================================================
     * ADD TASK
     * =====================================================
     */

    const addTaskForm = document.getElementById("add-task-form");

    if (addTaskForm) {

        addTaskForm.addEventListener("submit", async (event) => {

            event.preventDefault();

            const input = document.getElementById("task-title");
            const button = addTaskForm.querySelector("button");

            const title = input.value.trim();

            if (!title) {
                return;
            }

            const originalText = button.textContent;

            button.disabled = true;
            button.textContent = "Adding...";

            try {

                const response = await fetch(
                    addTaskForm.action,
                    {
                        method: "POST",
                        body: new FormData(addTaskForm)
                    }
                );

                const data = await response.json();

                if (!data.success) {
                    showMessage(data.message, "danger");
                    return;
                }

                addTaskToTable(data.task);

                input.value = "";

                showMessage(
                    data.message,
                    "success"
                );

            } catch (error) {

                console.error(error);

                showMessage(
                    "Something went wrong. Please try again.",
                    "danger"
                );

            } finally {

                button.disabled = false;
                button.textContent = originalText;

            }

        });

    }


    /*
     * =====================================================
     * NEXT / CHANGE STATUS
     * =====================================================
     */

    const taskActionForms = document.querySelectorAll(
        ".task-action-form"
    );

    taskActionForms.forEach((form) => {

        form.addEventListener("submit", async (event) => {

            event.preventDefault();

            const button = form.querySelector("button");

            const originalText = button.textContent;

            button.disabled = true;
            button.textContent = "...";

            try {

                const response = await fetch(
                    form.action,
                    {
                        method: "POST"
                    }
                );

                const data = await response.json();

                if (!data.success) {
                    showMessage(data.message, "danger");
                    return;
                }

                /*
                 * If this is a delete form,
                 * remove the row.
                 */

                if (form.classList.contains("delete-task-form")) {

                    const row = document.getElementById(
                        `task-row-${data.task_id}`
                    );

                    if (row) {

                        row.style.transition =
                            "opacity 0.25s ease, transform 0.25s ease";

                        row.style.opacity = "0";
                        row.style.transform = "translateX(20px)";

                        setTimeout(() => {

                            row.remove();

                            updateTaskNumbers();
                            checkEmptyState();

                        }, 250);

                    }

                }

                /*
                 * Otherwise this is the Next button.
                 */

                else {

                    updateTaskStatus(data.task);

                }

                showMessage(
                    data.message,
                    "success"
                );

            } catch (error) {

                console.error(error);

                showMessage(
                    "Something went wrong. Please try again.",
                    "danger"
                );

            } finally {

                button.disabled = false;
                button.textContent = originalText;

            }

        });

    });


    /*
     * =====================================================
     * CLEAR ALL TASKS
     * =====================================================
     */

    const clearTasksForm = document.getElementById(
        "clear-tasks-form"
    );

    if (clearTasksForm) {

        clearTasksForm.addEventListener("submit", async (event) => {

            event.preventDefault();

            const confirmed = confirm(
                "Are you sure you want to delete all tasks?"
            );

            if (!confirmed) {
                return;
            }

            const button = clearTasksForm.querySelector("button");

            const originalText = button.textContent;

            button.disabled = true;
            button.textContent = "Clearing...";

            try {

                const response = await fetch(
                    clearTasksForm.action,
                    {
                        method: "POST"
                    }
                );

                const data = await response.json();

                if (!data.success) {
                    showMessage(data.message, "danger");
                    return;
                }

                const tableBody = document.getElementById(
                    "task-table-body"
                );

                if (tableBody) {
                    tableBody.innerHTML = "";
                }

                checkEmptyState();

                showMessage(
                    data.message,
                    "info"
                );

            } catch (error) {

                console.error(error);

                showMessage(
                    "Something went wrong. Please try again.",
                    "danger"
                );

            } finally {

                button.disabled = false;
                button.textContent = originalText;

            }

        });

    }


    /*
     * =====================================================
     * ADD TASK TO TABLE
     * =====================================================
     */

    function addTaskToTable(task) {

            const emptyMessage = document.getElementById(
        "empty-task-message"
    );

    if (emptyMessage) {
        emptyMessage.remove();
    }

    let tableBody = document.getElementById(
        "task-table-body"
    );

        let tableBody = document.getElementById(
            "task-table-body"
        );

        /*
         * If there were no tasks before,
         * create the table.
         */

        if (!tableBody) {

            const taskBox = document.querySelector(".task-box");

            const emptyMessage = document.getElementById(
                "empty-task-message"
            );

            if (emptyMessage) {
                emptyMessage.remove();
            }

            const table = document.createElement("table");

            table.className = "task-table";

            table.innerHTML = `
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Task</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>

                <tbody id="task-table-body"></tbody>
            `;

            taskBox.appendChild(table);

            tableBody = document.getElementById(
                "task-table-body"
            );
        }


        const row = document.createElement("tr");

        row.id = `task-row-${task.id}`;

        row.innerHTML = `
            <td></td>

            <td class="task-title-cell">
                ${escapeHtml(task.title)}
            </td>

            <td>
                <span class="badge ${getStatusClass(task.status)}">
                    ${escapeHtml(task.status)}
                </span>
            </td>

            <td>

                <form
                    action="/tasks/toggle/${task.id}"
                    method="POST"
                    class="task-action-form"
                >
                    <button
                        class="btn-small"
                        type="submit"
                    >
                        Next
                    </button>
                </form>

                <form
                    action="/tasks/delete/${task.id}"
                    method="POST"
                    class="task-action-form delete-task-form"
                >
                    <button
                        class="btn-small btn-delete"
                        type="submit"
                    >
                        Delete
                    </button>
                </form>

            </td>
        `;


        tableBody.appendChild(row);

        attachActionEvents(row);

        updateTaskNumbers();

        const taskToolbar = document.getElementById("task-toolbar");

        if (taskToolbar) {
            taskToolbar.style.display = "flex";}

    }


    /*
     * =====================================================
     * UPDATE STATUS
     * =====================================================
     */

    function updateTaskStatus(task) {

        const row = document.getElementById(
            `task-row-${task.id}`
        );

        if (!row) {
            return;
        }

        const badge = row.querySelector(".badge");

        if (!badge) {
            return;
        }

        badge.className =
            `badge ${getStatusClass(task.status)}`;

        badge.textContent = task.status;

    }


    /*
     * =====================================================
     * ATTACH EVENTS TO NEW ROWS
     * =====================================================
     */

    function attachActionEvents(row) {

        const forms = row.querySelectorAll(
            ".task-action-form"
        );

        forms.forEach((form) => {

            form.addEventListener(
                "submit",
                handleTaskAction
            );

        });

    }


    /*
     * =====================================================
     * HANDLE TASK ACTION
     * =====================================================
     */

    async function handleTaskAction(event) {

        event.preventDefault();

        const form = event.currentTarget;

        const button = form.querySelector("button");

        const originalText = button.textContent;

        button.disabled = true;
        button.textContent = "...";

        try {

            const response = await fetch(
                form.action,
                {
                    method: "POST"
                }
            );

            const data = await response.json();

            if (!data.success) {

                showMessage(
                    data.message,
                    "danger"
                );

                return;
            }


            if (
                form.classList.contains(
                    "delete-task-form"
                )
            ) {

                const row = form.closest("tr");

                if (row) {

                    row.style.transition =
                        "opacity 0.25s ease, transform 0.25s ease";

                    row.style.opacity = "0";
                    row.style.transform =
                        "translateX(20px)";

                    setTimeout(() => {

                        row.remove();

                        updateTaskNumbers();
                        checkEmptyState();

                    }, 250);

                }

            } else {

                updateTaskStatus(data.task);

            }


            showMessage(
                data.message,
                "success"
            );

        } catch (error) {

            console.error(error);

            showMessage(
                "Something went wrong. Please try again.",
                "danger"
            );

        } finally {

            button.disabled = false;
            button.textContent = originalText;

        }

    }


    /*
     * =====================================================
     * UPDATE ROW NUMBERS
     * =====================================================
     */

    function updateTaskNumbers() {

        const rows = document.querySelectorAll(
            "#task-table-body tr"
        );

        rows.forEach((row, index) => {

            const numberCell = row.querySelector(
                "td:first-child"
            );

            if (numberCell) {
                numberCell.textContent = index + 1;
            }

        });

    }


    /*
     * =====================================================
     * EMPTY STATE
     * =====================================================
     */

function checkEmptyState() {

    const tableBody = document.getElementById(
        "task-table-body"
    );

    const taskCount = document.getElementById(
        "task-count"
    );

    const clearButton = document.getElementById(
        "clear-tasks-button"
    );

    const taskBox = document.querySelector(
        ".task-box"
    );

    const taskTotal = tableBody
        ? tableBody.querySelectorAll("tr").length
        : 0;


    /* Update counter */

    if (taskCount) {

        if (taskTotal === 1) {
            taskCount.textContent = "1 task";
        } else {
            taskCount.textContent = `${taskTotal} tasks`;
        }

    }


    /* Enable / disable Clear All */

    if (clearButton) {
        clearButton.disabled = taskTotal === 0;
    }


    /* If tasks still exist, we're finished */

    if (taskTotal > 0) {
        return;
    }


    /* Remove table */

    const tableWrapper = document.querySelector(
        ".task-table-wrapper"
    );

    if (tableWrapper) {
        tableWrapper.remove();
    }


    /* Show empty state */

    if (
        taskBox &&
        !document.getElementById(
            "empty-task-message"
        )
    ) {

        const message =
            document.createElement("div");

        message.id =
            "empty-task-message";

        message.className =
            "empty-task-state";

        message.innerHTML = `
            <div class="empty-task-icon">✓</div>

            <h3>No tasks yet</h3>

            <p>
                Add your first task above and
                start getting things done.
            </p>
        `;

        taskBox.appendChild(message);
    }

}


    /*
     * =====================================================
     * FLASH / TOAST MESSAGE
     * =====================================================
     */

    function showMessage(message, type = "success") {

        const existingMessages =
            document.querySelectorAll(
                ".dynamic-message"
            );

        existingMessages.forEach(
            (message) => message.remove()
        );


        const messageElement =
            document.createElement("div");

        messageElement.className =
            `flash ${type} dynamic-message`;

        messageElement.textContent =
            message;


        const main = document.querySelector(
            "main.container"
        );

        if (main) {

            main.insertBefore(
                messageElement,
                main.firstChild
            );

        }


        setTimeout(() => {

            messageElement.style.transition =
                "opacity 0.3s ease, transform 0.3s ease";

            messageElement.style.opacity = "0";
            messageElement.style.transform =
                "translateY(-8px)";

            setTimeout(() => {
                messageElement.remove();
            }, 300);

        }, 2500);

    }


    /*
     * =====================================================
     * STATUS CSS CLASS
     * =====================================================
     */

    function getStatusClass(status) {

        return status
            .toLowerCase()
            .replace(/\s+/g, "-");

    }


    /*
     * =====================================================
     * SECURITY
     * Escape user-generated task titles before putting
     * them into innerHTML.
     * =====================================================
     */

    function escapeHtml(value) {

        const div =
            document.createElement("div");

        div.textContent = value;

        return div.innerHTML;

    }

});