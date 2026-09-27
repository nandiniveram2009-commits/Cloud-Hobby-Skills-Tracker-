import React, { useState, useEffect } from 'react';

export default function App() {
  const [skills, setSkills] = useState([]);
  const [feed, setFeed] = useState([]);
  const [analytics, setAnalytics] = useState({});
  const [skillName, setSkillName] = useState('');
  const [postContent, setPostContent] = useState('');

  const API_URL = "http://localhost:8000";

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const skillsRes = await fetch(`${API_URL}/api/skills`);
      const skillsData = await skillsRes.json();
      setSkills(skillsData.skills || []);

      const feedRes = await fetch(`${API_URL}/api/feed`);
      const feedData = await feedRes.json();
      setFeed(feedData.feed || []);

      const analyticsRes = await fetch(`${API_URL}/api/analytics/dashboard`);
      const analyticsData = await analyticsRes.json();
      setAnalytics(analyticsData);
    } catch (err) {
      console.error("Error connecting to backend:", err);
    }
  };

  const handleAddSkill = async (e) => {
    e.preventDefault();
    await fetch(`${API_URL}/api/skills`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        skill_name: skillName,
        category: "General",
        current_level: "BEGINNER",
        target_level: "ADVANCED",
        target_date: "2025-12-31"
      })
    });
    setSkillName('');
    fetchData();
  };

  const handleCreatePost = async (e) => {
    e.preventDefault();
    await fetch(`${API_URL}/api/posts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: postContent })
    });
    setPostContent('');
    fetchData();
  };

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', padding: '20px', maxWidth: '800px', margin: 'auto' }}>
      <h1>🎸 Cloud Hobby & Skills Tracker</h1>
      
      <div style={{ background: '#f4f4f4', padding: '15px', borderRadius: '8px', marginBottom: '20px' }}>
        <h3>📊 Dashboard Analytics</h3>
        <p>Total Practice Hours: <strong>{analytics.total_practice_hours || 0} hrs</strong></p>
        <p>Active Skills: <strong>{analytics.active_skills_count || 0}</strong></p>
        <p>Current Streak: <strong>{analytics.current_streak_days || 0} Days 🔥</strong></p>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h3>Add New Hobby / Skill</h3>
        <form onSubmit={handleAddSkill}>
          <input 
            type="text" 
            placeholder="e.g. Photography, Guitar" 
            value={skillName} 
            onChange={(e) => setSkillName(e.target.value)}
            style={{ padding: '8px', width: '70%', marginRight: '10px' }}
            required
          />
          <button type="submit" style={{ padding: '8px 15px' }}>Add Skill</button>
        </form>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h3>Share Achievement to Community</h3>
        <form onSubmit={handleCreatePost}>
          <input 
            type="text" 
            placeholder="Share your progress..." 
            value={postContent} 
            onChange={(e) => setPostContent(e.target.value)}
            style={{ padding: '8px', width: '70%', marginRight: '10px' }}
            required
          />
          <button type="submit" style={{ padding: '8px 15px' }}>Post</button>
        </form>
      </div>

      <div>
        <h3>🌍 Community Feed</h3>
        {feed.length === 0 ? <p>No posts yet. Be the first to share!</p> : null}
        {feed.map((post) => (
          <div key={post.post_id} style={{ border: '1px solid #ddd', padding: '10px', borderRadius: '5px', marginBottom: '10px' }}>
            <p><strong>User ({post.user_id}):</strong> {post.content}</p>
            <small style={{ color: '#666' }}>{post.created_at}</small>
          </div>
        ))}
      </div>
    </div>
  );
    }
