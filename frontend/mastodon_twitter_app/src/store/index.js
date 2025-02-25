import { create } from "zustand";
import { postStatus,  fetchUserInfo ,deleteStatus} from "./services";

const useMastodonStore = create((set, get) => ({
  userInfo: null,
  userPosts: [],
  loading: false,
  error: null,
  page: 1,

  setStatus: (status) => set({ status }),

  fetchInitialData: async () => {
    try {
      set({ loading: true });
      const userResponse = await fetchUserInfo();
      // const postsResponse = await fetchUserPosts(1); // Fetch first page (20 posts)
      set({ userInfo: userResponse.data,
        //  userPosts: postsResponse.data, loading: false 
        });
    } catch (error) {
      set({ error: error.message, loading: false });
      console.error("Error fetching user data", error);
    }
  },

  loadMorePosts: async () => {
    try {
      
    } catch (error) {
      console.error("Error loading more posts", error);
    }
  },

  createPost: async (content) => {
    try {
      const response = await postStatus(content);
      set((state) => ({
        userPosts: [response.data, ...state.userPosts],
      }));
    } catch (error) {
      console.error("Error creating post", error);
    }
  },

  deletePost: async (postId) => {
    try {
      const response = await deleteStatus(postId);
      set((state) => ({
        userPosts: state.userPosts.filter((p) => p.id!== postId),
      }));
    } catch (error) {
      console.error("Error deleting post", error);
    }
  }

  
}));

export default useMastodonStore;
