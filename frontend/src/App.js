import React, { useEffect, useState } from "react";

function App() {
  const [tasks, setTasks] = useState([]);
  const [task, setTask] = useState("");

  const loadTasks = async () => {
    try {
      const res = await fetch("http://34.207.116.249:5000/tasks");
      const data = await res.json();
      setTasks(data);
    } catch (err) {
      console.log("Backend not running yet");
    }
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const handleAdd = async () => {
    if (!task) return;

    await fetch("http://34.207.116.249:5000/tasks", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ task }),
    });

    setTask("");
    loadTasks();
  };

  const handleDelete = async (id) => {
    await fetch(`http://34.207.116.249:5000/tasks/${id}`, {
      method: "DELETE",
    });

    loadTasks();
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Task Manager</h1>

      <input
        value={task}
        onChange={(e) => setTask(e.target.value)}
        placeholder="Enter task"
      />

      <button onClick={handleAdd}>Add</button>

      <ul>
        {tasks.map((t) => (
          <li key={t.id}>
            {t.task}
            <button onClick={() => handleDelete(t.id)}>❌</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;