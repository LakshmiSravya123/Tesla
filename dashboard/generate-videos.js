const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

const API = "https://tesla-dashboard-api.onrender.com";

// Prompts to generate videos for
const prompts = [
    {
        id: 'tesla_delivery',
        title: 'Tesla Delivery Day',
        prompt: 'Cinematic shot of excited person receiving Tesla Model Y keys at delivery center'
    },
    {
        id: 'autopilot_demo',
        title: 'Autopilot Demo',
        prompt: 'Inside Tesla, family amazed as steering wheel drives itself on highway'
    },
    {
        id: 'supercharger',
        title: 'Supercharger Speed',
        prompt: 'Tesla Supercharger station, rapid charging with battery percentage increasing'
    }
];

// Download file from URL
function downloadFile(url, filepath) {
    return new Promise((resolve, reject) => {
        const protocol = url.startsWith('https') ? https : http;
        const file = fs.createWriteStream(filepath);
        
        protocol.get(url, (response) => {
            if (response.statusCode === 302 || response.statusCode === 301) {
                // Handle redirect
                file.close();
                fs.unlinkSync(filepath);
                return downloadFile(response.headers.location, filepath)
                    .then(resolve)
                    .catch(reject);
            }
            
            response.pipe(file);
            file.on('finish', () => {
                file.close();
                console.log(`✅ Downloaded: ${filepath}`);
                resolve();
            });
        }).on('error', (err) => {
            fs.unlinkSync(filepath);
            reject(err);
        });
    });
}

// Generate video via API
async function generateVideo(prompt, model = 'hunyuan') {
    console.log(`\n🎬 Generating video: ${prompt.title}`);
    console.log(`Prompt: ${prompt.prompt}`);
    
    const response = await fetch(`${API}/api/generate-video`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: prompt.prompt, model })
    });
    
    if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
    }
    
    const data = await response.json();
    console.log(`Prediction ID: ${data.prediction_id || 'N/A'}`);
    
    return data;
}

// Poll for video completion
async function pollVideoStatus(predictionId) {
    const maxAttempts = 90; // 90 * 3 seconds = 4.5 minutes
    let attempts = 0;
    
    while (attempts < maxAttempts) {
        const response = await fetch(`${API}/api/video-status/${predictionId}`);
        
        if (response.ok) {
            const data = await response.json();
            console.log(`⏳ Status: ${data.status} (${attempts * 3}s elapsed)`);
            
            if (data.status === 'succeeded' && data.video_url) {
                return data.video_url;
            } else if (data.status === 'failed') {
                throw new Error(data.error || 'Video generation failed');
            }
        }
        
        await new Promise(resolve => setTimeout(resolve, 3000));
        attempts++;
    }
    
    throw new Error('Video generation timed out');
}

// Main function
async function main() {
    console.log('🚀 Starting video generation process...\n');
    
    const videosDir = path.join(__dirname, 'videos');
    if (!fs.existsSync(videosDir)) {
        fs.mkdirSync(videosDir);
    }
    
    const generatedVideos = [];
    
    for (const prompt of prompts) {
        try {
            // Generate video
            const result = await generateVideo(prompt);
            
            if (result.prediction_id) {
                // Poll for completion
                const videoUrl = await pollVideoStatus(result.prediction_id);
                
                // Download video
                const filename = `${prompt.id}.mp4`;
                const filepath = path.join(videosDir, filename);
                
                console.log(`📥 Downloading video to: ${filepath}`);
                await downloadFile(videoUrl, filepath);
                
                generatedVideos.push({
                    id: prompt.id,
                    title: prompt.title,
                    prompt: prompt.prompt,
                    filename: filename,
                    filepath: `videos/${filename}`,
                    video_url: videoUrl
                });
                
            } else if (result.video_url) {
                // Direct URL (demo mode)
                const filename = `${prompt.id}.mp4`;
                const filepath = path.join(videosDir, filename);
                
                console.log(`📥 Downloading video to: ${filepath}`);
                await downloadFile(result.video_url, filepath);
                
                generatedVideos.push({
                    id: prompt.id,
                    title: prompt.title,
                    prompt: prompt.prompt,
                    filename: filename,
                    filepath: `videos/${filename}`,
                    video_url: result.video_url
                });
            }
            
        } catch (error) {
            console.error(`❌ Error generating ${prompt.title}:`, error.message);
        }
    }
    
    // Save metadata
    const metadataPath = path.join(videosDir, 'metadata.json');
    fs.writeFileSync(metadataPath, JSON.stringify(generatedVideos, null, 2));
    console.log(`\n✅ Saved metadata to: ${metadataPath}`);
    
    console.log(`\n🎉 Generated ${generatedVideos.length}/${prompts.length} videos successfully!`);
}

main().catch(console.error);
