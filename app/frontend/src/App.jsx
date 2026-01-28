import { useEffect, useState } from "react";

const API = "http://backend:5000";

export default function App() {
  const [notes, setNotes] = useState([]);
  const [text, setText] = useState("");

  const loadNotes = async () => {
    const res = await fetch(`${API}/api/notes`);
    const data = await res.json();
    setNotes(data);
  };

  const addNote = async () => {
    await fetch(`${API}/api/notes`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ note: text }),
    });
    setText("");
    loadNotes();
  };

  useEffect(() => {
    loadNotes();
  }, []);

  return (
    <div style={{ padding: 40 }}>
      <h1>Notes App</h1>
      <input value={text} onChange={e => setText(e.target.value)} />
      <button onClick={addNote}>Add</button>

      <ul>
        {notes.map((n, i) => <li key={i}>{n}</li>)}
      </ul>
    </div>
  );
}
