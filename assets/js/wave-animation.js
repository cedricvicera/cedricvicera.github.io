/**
 * Layered Sine Wave Animation
 * Inspired by geometry, flow, and the merging of forms
 * Vanilla JavaScript implementation for static sites
 */

(function() {
  'use strict';
  
  // Wait for DOM to be ready
  function initWaveAnimation() {
    const canvas = document.getElementById('wave-canvas');
    if (!canvas) {
      console.warn('Wave canvas element not found');
      return;
    }
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    // Animation parameters
    const config = {
      layers: 80,
      points: 200,
      waveAmplitude: 40,
      timeSpeed: 0.01,
      backgroundColor: '#F0EEE6',
      strokeColor: '50, 50, 50', // RGB values for grayscale
      verticalLineSpacing: 20,
      verticalLineProbability: 0.4
    };
    
    let time = 0;
    let animationId = null;
    
    function drawWaves() {
      // Clear and fill background
      ctx.clearRect(0, 0, width, height);
      ctx.fillStyle = config.backgroundColor;
      ctx.fillRect(0, 0, width, height);
      
      // Increment time for animation
      time += config.timeSpeed;
      
      // Draw each layer - forms emerging from the formless
      for (let layer = 0; layer < config.layers; layer++) {
        const layerPosition = (layer / config.layers) * height * 0.8 + height * 0.1;
        const layerFrequency = 0.5 + layer * 0.03;
        const layerPhase = time * 0.2 + layer * 0.05;
        const layerAmplitude = config.waveAmplitude * (0.5 + 0.5 * Math.sin(layer * 0.1 + time * 0.3));
        
        // Calculate opacity with time-based variation
        const baseOpacity = 0.2 + 0.6 * Math.pow(Math.sin((layer / config.layers) * Math.PI), 2);
        const timeEffect = 0.2 * Math.sin(time * 0.4 + layer * 0.1);
        const opacity = Math.min(0.9, Math.max(0.1, baseOpacity + timeEffect));
        
        ctx.beginPath();
        ctx.strokeStyle = `rgba(${config.strokeColor}, ${opacity})`;
        ctx.lineWidth = 0.6;
        
        // Generate wave points
        for (let i = 0; i <= config.points; i++) {
          const x = (i / config.points) * width;
          
          // Create complex wave with multiple sine components
          let y = layerPosition;
          
          // Primary wave
          y += layerAmplitude * Math.sin(x * 0.01 * layerFrequency + layerPhase);
          
          // Secondary waves for complexity
          y += layerAmplitude * 0.3 * Math.sin(x * 0.02 * layerFrequency + layerPhase * 1.5);
          y += layerAmplitude * 0.2 * Math.sin(x * 0.04 * layerFrequency - layerPhase * 0.7);
          
          // Tertiary high-frequency detail
          y += layerAmplitude * 0.1 * Math.sin(x * 0.08 * layerFrequency + layerPhase * 2.3);
          
          if (i === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        }
        
        ctx.stroke();
      }
      
      // Draw connecting vertical lines - all merging into oneness
      for (let i = 0; i < width; i += config.verticalLineSpacing) {
        if (Math.random() < config.verticalLineProbability) {
          ctx.beginPath();
          
          const opacity = 0.1 + 0.2 * Math.sin(i * 0.05 + time);
          ctx.strokeStyle = `rgba(${config.strokeColor}, ${opacity})`;
          ctx.lineWidth = 0.3;
          
          // Vary the line height
          const startY = height * 0.1 + Math.random() * height * 0.2;
          const endY = height * 0.7 + Math.random() * height * 0.2;
          
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
