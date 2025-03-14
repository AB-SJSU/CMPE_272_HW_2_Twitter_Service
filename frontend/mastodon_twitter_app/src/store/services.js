import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL; // Replace with actual Mastodon instance
// const ACCESS_TOKEN = "your-access-token"; // Replace with your actual access token

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
//   headers: { Authorization: `Bearer ${ACCESS_TOKEN}` },
});

// Fetch user account details
export const fetchUserInfo = async () => {
  return await axiosInstance.get("/user");
};

// Fetch user account posts
export const fetchUserPosts = async (pageNo) => {
  return await axiosInstance.get("/retrieve_all?page=" + pageNo);
};


// Create a new post (status update)
export const postStatus = async (status) => {
  return await axiosInstance.post("/create", { content:status });
};

// delete a  post (status)
export const deleteStatus = async (postId) => {
  return await axiosInstance.delete(`/delete/${postId}`);
};


