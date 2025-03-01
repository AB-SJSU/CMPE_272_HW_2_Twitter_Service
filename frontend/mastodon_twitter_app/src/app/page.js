"use client";

import { useEffect, useRef } from "react";
import useMastodonStore from "../store";
import PostTextInput from "./components/post-textinput";
import PostItem from "./components/post-item";

// @author Aakruti
export default function MastodonApp() {
  const loader = useRef(null); // Reference to the loading div
  const { userInfo, userPosts, fetchInitialData, deletePost, loadMorePosts } =
    useMastodonStore();

  useEffect(() => {
    fetchInitialData();
  }, []);

  // Observe the loader div to trigger fetching more posts
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          loadMorePosts(); // Call API when loader is visible
        }
      },
      { threshold: 1 }
    );

    if (loader.current) {
      observer.observe(loader.current);
    }

    return () => {
      if (loader.current) {
        observer.unobserve(loader.current);
      }
    };
  }, [loadMorePosts]);

  return (
    <div className="flex flex-col items-center p-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold mb-4 text-green-600">
        Mastodon Twitter Service
      </h1>
      {userInfo && (
        <div className="mb-6 p-4 bg-white shadow-md rounded-md w-full max-w-md flex items-center space-x-4">
          <img
            src={userInfo.avatar}
            alt="User Avatar"
            className="w-10 h-10 rounded-full"
          />
          <p className="text-gray-700 font-medium">{userInfo.username}</p>
        </div>
      )}
      <div className="w-full max-w-md p-4 bg-white shadow-md rounded-md">
        <PostTextInput />
      </div>
      <div className="mt-6 w-full max-w-md h-96 overflow-y-auto">
        {userPosts.map((p) => (
          <PostItem
          key={p.id}
            id={p.id}
            content={p.content}
            createdAt={p.created_at}
            onDelete={() => deletePost(p.id)}
          />
        ))}
        {/* Loader for triggering API call when in view */}
        <div ref={loader} className="text-center p-4">
          Loading more...
        </div>
      </div>
    </div>
  );
}
