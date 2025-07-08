/**
 * Responsive utilities for the application
 * This file contains hooks and utilities to handle responsive design
 */

import { useState, useEffect } from 'react';

// Breakpoint definitions (matching Tailwind's default breakpoints)
export const BREAKPOINTS = {
  sm: 640,   // Small devices (phones)
  md: 768,   // Medium devices (tablets)
  lg: 1024,  // Large devices (desktops)
  xl: 1280,  // Extra large devices (large desktops)
  '2xl': 1536 // 2X Extra large devices
};

/**
 * Hook to detect current screen size and return responsive breakpoint
 * @returns {Object} Object containing current breakpoint and boolean flags for each breakpoint
 */
export const useBreakpoint = () => {
  // Initialize with default state
  const [breakpoint, setBreakpoint] = useState({
    current: 'base', // base, sm, md, lg, xl, 2xl
    isMobile: true,   // true if screen width < md
    isTablet: false,  // true if screen width >= md && < lg
    isDesktop: false, // true if screen width >= lg
    width: typeof window !== 'undefined' ? window.innerWidth : 0
  });

  useEffect(() => {
    // Skip if not in browser environment
    if (typeof window === 'undefined') return;

    const calculateBreakpoint = () => {
      const width = window.innerWidth;
      
      let current = 'base';
      if (width >= BREAKPOINTS['2xl']) current = '2xl';
      else if (width >= BREAKPOINTS.xl) current = 'xl';
      else if (width >= BREAKPOINTS.lg) current = 'lg';
      else if (width >= BREAKPOINTS.md) current = 'md';
      else if (width >= BREAKPOINTS.sm) current = 'sm';
      
      setBreakpoint({
        current,
        isMobile: width < BREAKPOINTS.md,
        isTablet: width >= BREAKPOINTS.md && width < BREAKPOINTS.lg,
        isDesktop: width >= BREAKPOINTS.lg,
        width
      });
    };

    // Calculate on mount
    calculateBreakpoint();

    // Add resize listener
    window.addEventListener('resize', calculateBreakpoint);
    
    // Clean up
    return () => window.removeEventListener('resize', calculateBreakpoint);
  }, []);

  return breakpoint;
};

/**
 * Hook to conditionally render components based on screen size
 * @returns {Object} Object containing functions to conditionally render components
 */
export const useResponsiveRendering = () => {
  const { isMobile, isTablet, isDesktop } = useBreakpoint();
  
  return {
    /**
     * Renders content only on mobile devices
     * @param {ReactNode} content - Content to render on mobile
     * @returns {ReactNode|null} Content or null
     */
    renderOnMobile: (content) => isMobile ? content : null,
    
    /**
     * Renders content only on tablet devices
     * @param {ReactNode} content - Content to render on tablet
     * @returns {ReactNode|null} Content or null
     */
    renderOnTablet: (content) => isTablet ? content : null,
    
    /**
     * Renders content only on desktop devices
     * @param {ReactNode} content - Content to render on desktop
     * @returns {ReactNode|null} Content or null
     */
    renderOnDesktop: (content) => isDesktop ? content : null,
    
    /**
     * Renders different content based on device type
     * @param {Object} options - Rendering options
     * @param {ReactNode} options.mobile - Content for mobile
     * @param {ReactNode} options.tablet - Content for tablet
     * @param {ReactNode} options.desktop - Content for desktop
     * @returns {ReactNode} Appropriate content for current device
     */
    renderResponsive: ({ mobile, tablet, desktop }) => {
      if (isMobile) return mobile;
      if (isTablet) return tablet || desktop; // Fallback to desktop if tablet not provided
      return desktop;
    }
  };
};

/**
 * Utility to generate responsive class names based on breakpoints
 * @param {Object} classNames - Object with breakpoint keys and class values
 * @returns {String} Combined class names string
 * 
 * Example usage:
 * const className = responsiveClasses({
 *   base: 'text-sm p-2',
 *   md: 'text-base p-4',
 *   lg: 'text-lg p-6'
 * });
 */
export const responsiveClasses = (classNames) => {
  if (!classNames || typeof classNames !== 'object') {
    return '';
  }
  
  // Start with base classes
  let result = classNames.base || '';
  
  // Add responsive classes using Tailwind's responsive prefixes
  if (classNames.sm) result += ` sm:${classNames.sm}`;
  if (classNames.md) result += ` md:${classNames.md}`;
  if (classNames.lg) result += ` lg:${classNames.lg}`;
  if (classNames.xl) result += ` xl:${classNames.xl}`;
  if (classNames['2xl']) result += ` 2xl:${classNames['2xl']}`;
  
  return result;
};