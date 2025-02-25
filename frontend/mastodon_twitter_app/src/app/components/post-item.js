import { Trash2 } from "lucide-react";
import { formatDistanceToNow } from "date-fns";
const PostItem = ({ content,id,createdAt, onDelete }) => {
    const relativeTime = formatDistanceToNow(new Date(createdAt), { addSuffix: true });
    return (
        <div key={id} className="p-4 bg-white text-black shadow-md rounded-md mt-2 flex justify-between items-center">
        <div>
       <div dangerouslySetInnerHTML={{ __html: content }}></div>
        <p className="text-gray-500 text-sm mt-1">{relativeTime}</p>
        </div>
        <button
        onClick={onDelete}
        className="bg-red-500 text-white px-3 py-1 rounded-md hover:bg-red-600 transition"
      >
        <Trash2 className="w-5 h-5" />
      </button>
      </div>
    );
  };
  
  export default PostItem;