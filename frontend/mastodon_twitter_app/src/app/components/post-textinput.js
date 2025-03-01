import { useState } from "react";
import useMastodonStore from "../../store";
import { Send, Image, Smile } from "lucide-react";

// @author Aakruti
export default function PostTextInput() {
  const [status, setStatus] = useState("");
  const {
    createPost
  } = useMastodonStore();

 

  const handlePost = async () => {
    try {
      const response = await createPost(status);
        setStatus("")
    } catch (error) {
      console.error("Error posting status", error);
    }
  };

  

  return (
    <div>
      <textarea
        className="w-full p-2 border rounded-md bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-400 placeholder-gray-500"
        placeholder="What's on your mind..."
        value={status}
        onKeyDown={(e) => {
        if (e.key === "Enter" && !e.shiftKey) {
          e.preventDefault(); // Prevents a new line in the textarea
          handlePost(); // Calls the post function
        }
      }}
        onChange={(e) => setStatus(e.target.value)}
      />
      <div className="flex items-center justify-between mt-3">
        <div className="flex space-x-2"/>

        <button
          className={`px-4 py-2 rounded-md flex items-center space-x-2 ${
            status.length==0 ? "bg-gray-400 cursor-not-allowed" : "bg-blue-500 hover:bg-blue-600"
  } text-white`}
          onClick={handlePost}
          disabled={status.length==0}
        >
          <Send className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
}
