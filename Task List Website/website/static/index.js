function deleteTask(taskId) {
    //send request POST to delete task endpoint
    fetch("/delete-task", {
        method: "POST",
        body: JSON.stringify({ taskId: taskId }),
    }).then((_res) => {
        //reloads window to home, just refreshes
        //after the responce is recieved
        window.location.href = "/";
    });
}