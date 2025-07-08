import React, { useEffect, useRef, useLayoutEffect } from 'react';

/**
 * SalesChart component for rendering sales data visualizations
 * This component creates a responsive chart that works across browsers
 * including Firefox which had rendering issues previously
 */
const SalesChart = ({ data, type = 'bar', height = 300, width = '100%' }) => {
  const canvasRef = useRef(null);
  const containerRef = useRef(null);
  
  // Function to render chart
  const renderChart = () => {
    if (!canvasRef.current || !data) return;
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    // Clear previous chart
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Get dimensions
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    
    // Ensure we have valid dimensions
    const chartWidth = rect.width > 0 ? rect.width : containerRef.current?.clientWidth || 300;
    const chartHeight = rect.height > 0 ? rect.height : height;
    
    // Set canvas dimensions
    canvas.width = chartWidth * dpr;
    canvas.height = chartHeight * dpr;
    
    // Scale context
    ctx.scale(dpr, dpr);
    
    // Draw chart based on type
    if (type === 'bar') {
      drawBarChart(ctx, data, chartWidth, chartHeight);
    } else if (type === 'line') {
      drawLineChart(ctx, data, chartWidth, chartHeight);
    } else if (type === 'pie') {
      drawPieChart(ctx, data, Math.min(chartWidth, chartHeight) / 2);
    }
  };
  
  // Use useLayoutEffect for DOM measurements before browser paint
  useLayoutEffect(() => {
    if (!canvasRef.current || !data) return;
    
    const canvas = canvasRef.current;
    
    // Set canvas style dimensions
    canvas.style.width = '100%';
    canvas.style.height = `${height}px`;
    
    // Initial render
    renderChart();
    
    // Setup ResizeObserver for responsive behavior
    // This is especially important for Firefox which has issues with canvas resizing
    const resizeObserver = new ResizeObserver(() => {
      renderChart();
    });
    
    // Observe both the canvas and its container
    if (containerRef.current) {
      resizeObserver.observe(containerRef.current);
    }
    
    // Handle window resize events
    const handleResize = () => {
      renderChart();
    };
    
    window.addEventListener('resize', handleResize);
    
    // Cleanup function
    return () => {
      resizeObserver.disconnect();
      window.removeEventListener('resize', handleResize);
      
      if (canvasRef.current) {
        const ctx = canvasRef.current.getContext('2d');
        ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
      }
    };
  }, [data, type, height, width]);
  
  // Bar chart drawing function
  const drawBarChart = (ctx, data, width, height) => {
    const padding = 40;
    const chartWidth = width - (padding * 2);
    const chartHeight = height - (padding * 2);
    const barWidth = chartWidth / data.labels.length;
    
    // Find max value for scaling
    const maxValue = Math.max(...data.datasets[0].data);
    const scale = chartHeight / maxValue;
    
    // Draw axes
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, height - padding);
    ctx.lineTo(width - padding, height - padding);
    ctx.strokeStyle = '#333';
    ctx.stroke();
    
    // Draw bars
    data.labels.forEach((label, index) => {
      const value = data.datasets[0].data[index];
      const barHeight = value * scale;
      const x = padding + (index * barWidth) + (barWidth * 0.1);
      const y = height - padding - barHeight;
      
      // Draw bar
      ctx.fillStyle = data.datasets[0].backgroundColor[index] || '#4299e1';
      ctx.fillRect(x, y, barWidth * 0.8, barHeight);
      
      // Draw label
      ctx.fillStyle = '#333';
      ctx.font = '12px Arial';
      ctx.textAlign = 'center';
      ctx.fillText(label, x + (barWidth * 0.4), height - padding + 20);
      
      // Draw value
      ctx.fillText(value.toString(), x + (barWidth * 0.4), y - 10);
    });
  };
  
  // Line chart drawing function
  const drawLineChart = (ctx, data, width, height) => {
    const padding = 40;
    const chartWidth = width - (padding * 2);
    const chartHeight = height - (padding * 2);
    
    // Find max value for scaling
    const maxValue = Math.max(...data.datasets[0].data);
    const scale = chartHeight / maxValue;
    
    // Draw axes
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, height - padding);
    ctx.lineTo(width - padding, height - padding);
    ctx.strokeStyle = '#333';
    ctx.stroke();
    
    // Draw line
    ctx.beginPath();
    const pointWidth = chartWidth / (data.labels.length - 1);
    
    data.datasets[0].data.forEach((value, index) => {
      const x = padding + (index * pointWidth);
      const y = height - padding - (value * scale);
      
      if (index === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
      
      // Draw point
      ctx.fillStyle = '#4299e1';
      ctx.beginPath();
      ctx.arc(x, y, 4, 0, Math.PI * 2);
      ctx.fill();
      
      // Draw label
      ctx.fillStyle = '#333';
      ctx.font = '12px Arial';
      ctx.textAlign = 'center';
      ctx.fillText(data.labels[index], x, height - padding + 20);
    });
    
    ctx.strokeStyle = '#4299e1';
    ctx.lineWidth = 2;
    ctx.stroke();
  };
  
  // Pie chart drawing function
  const drawPieChart = (ctx, data, radius) => {
    const centerX = ctx.canvas.width / (2 * window.devicePixelRatio);
    const centerY = ctx.canvas.height / (2 * window.devicePixelRatio);
    
    let total = data.datasets[0].data.reduce((sum, value) => sum + value, 0);
    let startAngle = 0;
    
    data.datasets[0].data.forEach((value, index) => {
      const sliceAngle = (2 * Math.PI * value) / total;
      
      // Draw slice
      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.arc(centerX, centerY, radius, startAngle, startAngle + sliceAngle);
      ctx.closePath();
      ctx.fillStyle = data.datasets[0].backgroundColor[index] || `hsl(${index * 30}, 70%, 60%)`;
      ctx.fill();
      
      // Draw label
      const labelAngle = startAngle + (sliceAngle / 2);
      const labelX = centerX + (radius * 0.7 * Math.cos(labelAngle));
      const labelY = centerY + (radius * 0.7 * Math.sin(labelAngle));
      
      ctx.fillStyle = '#fff';
      ctx.font = '12px Arial';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(data.labels[index], labelX, labelY);
      
      startAngle += sliceAngle;
    });
  };
  
  return (
    <div className="sales-chart-container" ref={containerRef} style={{ width, height }}>
      <canvas 
        ref={canvasRef} 
        className="sales-chart"
        style={{ display: 'block', width: '100%', height: '100%' }}
      />
    </div>
  );
};

export default SalesChart;