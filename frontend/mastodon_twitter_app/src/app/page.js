'use client'

import { useState,useEffect } from "react";
import useMastodonStore from "../store";
import PostTextInput from "./components/post-textinput";
import PostItem from "./components/post-item";

export default function MastodonApp() {
  const {
    userInfo,
    userPosts,
    fetchInitialData,
    deletePost
  } = useMastodonStore();

  useEffect(() => {
    fetchInitialData();
  }, []);

  return (
    <div className="flex flex-col items-center p-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold mb-4 text-green-600">Mastodon Twitter Service</h1>
      {userInfo && (
        <div className="mb-6 p-4 bg-white shadow-md rounded-md w-full max-w-md flex items-center space-x-4">
          <img src={userInfo.avatar} alt="User Avatar" className="w-10 h-10 rounded-full" />
          <p className="text-gray-700 font-medium">{userInfo.username}</p>
        </div>
      )}
      <div className="w-full max-w-md p-4 bg-white shadow-md rounded-md">
      <PostTextInput/>
    </div>
      <div className="mt-6 w-full max-w-md">
          {userPosts.map((p) => (
            <PostItem id={p.id} content={p.content}
            createdAt={p.created_at} onDelete={()=> deletePost(p.id) }/>
          ))}
      </div>
    </div>
  );
}
