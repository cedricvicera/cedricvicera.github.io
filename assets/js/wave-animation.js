/**
 * Layered Sine Wave Animation - Custom Version
 * Modified for unique rectangular design with enhanced movement
 */

(function() {
  'use strict';
  
  function initWaveAnimation() {
    const canvas = document.getElementById('wave-canvas');
    if (!canvas) {
      console.warn('Wave canvas element not found');
      return;
    }
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    // Animation parameters - customized for unique look
    const config = {
      layers: 65,                      // Adjusted for rectangular format
      points: 250,                     // Smoother waves
      waveAmplitude: 35,               // Slightly reduced for elegance
      timeSpeed: 0.025,                // FASTER - increased from 0.01
      backgroundColor: '#F0EEE6',      // Your background color
      strokeColor: '80, 75, 70',       // Warmer gray-brown (instead of 50,50,50)
      verticalLineSpacing: 25,         // Slightly wider spacing
      verticalLineProbability: 0.3,    // Fewer vertical lines for cleaner look
      horizontalFlow: 1.2              // NEW - adds horizontal drift
    };
    
    let time = 0;
    let animationId = null;
    
    function drawWaves() {
      // Clear and fill background
      ctx.clearRect(0, 0, width, height);
      ctx.fillStyle = config.backgroundColor;
      ctx.fillRect(0, 0, width, height);
      
      // Increment time for animation - FASTER
      time += config.timeSpeed;
      
      // Draw each layer with enhanced movement
      for (let layer = 0; layer < config.layers; layer++) {
        const layerPosition = (layer / config.layers) * height * 0.75 + height * 0.125;
        const layerFrequency = 0.4 + layer * 0.025;  // Slightly adjusted
        const layerPhase = time * 0.3 + layer * 0.06; // Faster phase shift
        const layerAmplitude = config.waveAmplitude * (0.6 + 0.4 * Math.sin(layer * 0.12 + time * 0.4));
        
        // More dynamic opacity variation
        const baseOpacity = 0.15 + 0.65 * Math.pow(Math.sin((layer / config.layers) * Math.PI), 2);
        const timeEffect = 0.25 * Math.sin(time * 0.5 + layer * 0.15);
        const opacity = Math.min(0.85, Math.max(0.08, baseOpacity + timeEffect));
        
        ctx.beginPath();
        ctx.strokeStyle = `rgba(${config.strokeColor}, ${opacity})`;
        ctx.lineWidth = 0.7;
        
        // Generate wave points with horizontal drift
        for (let i = 0; i <= config.points; i++) {
          const x = (i / config.points) * width;
          
          // Horizontal drift effect
          const drift = Math.sin(time * 0.15 + layer * 0.1) * 15;
          
          // Create complex wave with multiple sine components
          let y = layerPosition;
          
          // Primary wave with drift
          y += layerAmplitude * Math.sin((x + drift) * 0.009 * layerFrequency + layerPhase);
          
          // Secondary waves for complexity
          y += layerAmplitude * 0.35 * Math.sin((x + drift * 0.7) * 0.018 * layerFrequency + layerPhase * 1.6);
          y += layerAmplitude * 0.25 * Math.sin((x + drift * 1.3) * 0.035 * layerFrequency - layerPhase * 0.8);
          
          // Tertiary high-frequency detail
          y += layerAmplitude * 0.12 * Math.sin((x + drift * 0.5) * 0.07 * layerFrequency + layerPhase * 2.4);
          
          if (i === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        }
        
        ctx.stroke();
      }
      
      // Draw connecting vertical lines - fewer and more subtle
      for (let i = 0; i < width; i += config.verticalLineSpacing) {
        if (Math.random() < config.verticalLineProbability) {
          ctx.beginPath();
          
          const opacity = 0.08 + 0.15 * Math.sin(i * 0.04 + time);
          ctx.strokeStyle = `rgba(${config.strokeColor}, ${opacity})`;
          ctx.lineWidth = 0.4;
          
          // Vary the line height with movement
          const startY = height * 0.15 + Math.random() * height * 0.15 + Math.sin(time + i * 0.1) * 10;
          const endY = height * 0.65 + Math.random() * height * 0.15 + Math.sin(time * 0.8 + i * 0.1) * 10;
          
          ctx.moveTo(i, startY);
          ctx.lineTo(i, endY);
          ctx.stroke();
        }
      }
      
      // Continue animation loop
      animationId = requestAnimationFrame(drawWaves);
    }
    
    // Start animation
    animationId = requestAnimationFrame(drawWaves);
    
    // Cleanup on page unload
    window.addEventListener('beforeunload', function() {
      if (animationId) {
        cancelAnimationFrame(animationId);
      }
    });
    
    // Pause animation when page is hidden (performance optimization)
    document.addEventListener('visibilitychange', function() {
      if (document.hidden) {
        if (animationId) {
          cancelAnimationFrame(animationId);
          animationId = null;
        }
      } else {
        if (!animationId) {
          animationId = requestAnimationFrame(drawWaves);
        }
      }
    });
  }
  
  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initWaveAnimation);
  } else {
    initWaveAnimation();
  }
})();