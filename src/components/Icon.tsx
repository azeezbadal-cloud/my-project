import React from 'react';
import {HandHeart, MessageCircleHeart, MoonStar, ShoppingBag, SprayCan, UsersRound, Car} from 'lucide';
import type {IconName} from '../config';
import {clamp01, easeOutCubic} from '../lib/anim';

type IconNode = [string, Record<string, string | number>][];

// Register any extra lucide icon here, then use its name in src/config.ts
const ICONS: Record<IconName, IconNode> = {
  HandHeart: HandHeart as unknown as IconNode,
  UsersRound: UsersRound as unknown as IconNode,
  Car: Car as unknown as IconNode,
  ShoppingBag: ShoppingBag as unknown as IconNode,
  SprayCan: SprayCan as unknown as IconNode,
  MessageCircleHeart: MessageCircleHeart as unknown as IconNode,
  MoonStar: MoonStar as unknown as IconNode,
};

type Props = {
  name: IconName;
  size: number;
  /** 0 → 1 : strokes draw themselves on, one after another */
  draw: number;
  color: string;
  glow?: string;
  strokeWidth?: number;
  /** 0..1 soft fill that fades in once drawn */
  fill?: number;
};

/** Minimal line icon whose strokes draw on (stroke-dashoffset) – with a soft glow once complete. */
export const Icon: React.FC<Props> = ({name, size, draw, color, glow, strokeWidth = 1.7, fill = 0}) => {
  const node = ICONS[name];
  const n = node.length;
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke={color}
      strokeWidth={strokeWidth}
      strokeLinecap="round"
      strokeLinejoin="round"
      style={{overflow: 'visible', filter: glow ? `drop-shadow(0 0 ${size * 0.14}px ${glow})` : undefined}}
    >
      {node.map(([tag, attrs], i) => {
        const p = easeOutCubic(clamp01((draw - i * (0.45 / n)) / 0.55));
        return React.createElement(tag, {
          key: i,
          ...attrs,
          pathLength: 1,
          strokeDasharray: '1 1',
          strokeDashoffset: 1 - p,
          fill: fill > 0 && tag === 'path' ? color : 'none',
          fillOpacity: fill > 0 ? fill * 0.16 : 0,
        });
      })}
    </svg>
  );
};
