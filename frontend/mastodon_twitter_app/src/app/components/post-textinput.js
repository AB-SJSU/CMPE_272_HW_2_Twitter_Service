import { useState } from "react";
import useMastodonStore from "../../store";
import { Send, Image, Smile } from "lucide-react";

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
        <div className="flex space-x-2">
          {/* <button className="p-2 rounded-full text-gray-600 hover:text-blue-500">
            <Image className="w-5 h-5" />
          </button>
          <button className="p-2 rounded-full text-gray-600 hover:text-blue-500">
            <Smile className="w-5 h-5" />
          </button> */}
        </div>
        <button
          className="bg-blue-500 text-white px-4 py-2 rounded-md flex items-center space-x-2 hover:bg-blue-600"
          onClick={handlePost}
        >
          <Send className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
}
