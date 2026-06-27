const taskInput = document.getElementById("taskInput");
const addBtn = document.getElementById("addBtn");
const taskList = document.getElementById("taskList");


// CREATE
async function addTask() {

    let task = taskInput.value.trim();

    if(task === ""){
        alert("Enter a task");
        return;
    }

    await fetch("/add",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            task:task
        })
    });

    taskInput.value = "";

    loadTasks();
}

// READ
async function loadTasks(){

    const response = await fetch("/tasks");

    const tasks = await response.json();

    console.log(tasks); // Add this line

    taskList.innerHTML = "";

    tasks.forEach(task => {

        const li = document.createElement("li");
li.innerHTML = `
    <span>${task.task}</span>

    <div class="btn-group">
        <button class="edit-btn"
                onclick="editTask(${task.id})">
            Edit
        </button>

        <button class="delete-btn"
                onclick="deleteTask(${task.id})">
            Delete
        </button>
    </div>
`;
        taskList.appendChild(li);
    });
}

// DELETE
async function deleteTask(id){

    await fetch(`/delete/${id}`,{
        method:"DELETE"
    });

    loadTasks();
}

async function editTask(id){

    const newTask = prompt("Enter new task");

    if(!newTask) return;

    await fetch(`/update/${id}`,{
        method:"PUT",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            task:newTask
        })
    });

    loadTasks();
}

// Button Click
addBtn.addEventListener("click", addTask);

// Initial Load
loadTasks();