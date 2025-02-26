import { create } from "zustand";
import {
  postStatus,
  fetchUserInfo,
  deleteStatus,
  fetchUserPosts,
} from "./services";

const useMastodonStore = create((set, get) => ({
  userInfo: null,
  userPosts: [],
  loading: false,
  error: null,
  page: 1,
  hasNextPostPage: true,

  setStatus: (status) => set({ status }),

  fetchInitialData: async () => {
    try {
      set({ loading: true });
      const userResponse = await fetchUserInfo();
      const postsResponse = await fetchUserPosts(1); // Fetch first page (20 posts)
      set({
        userInfo: userResponse.data,
        userPosts: postsResponse.data.posts,
        loading: false,
        hasNextPostPage: postsResponse.data.has_next,
        page: get().page + 1,
      });
    } catch (error) {
      set({ error: error.message, loading: false });
      console.error("Error fetching user data", error);
    }
  },

  loadMorePosts: async () => {
    try {
      
      if (get().hasNextPostPage && get().loading === false) {
        set({ loading: true });
        const postsResponse = await fetchUserPosts(get().page); // Fetch next page
        set((state) => ({
          userPosts: [...state.userPosts, ...postsResponse.data.posts],
          hasNextPostPage: postsResponse.data.has_next,
          page: get().page + 1, // Update page number after loading more posts
          loading: false,
        }));
      }
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
        userPosts: state.userPosts.filter((p) => p.id !== postId),
      }));
    } catch (error) {
      console.error("Error deleting post", error);
    }
  },
}));

export default useMastodonStore;
