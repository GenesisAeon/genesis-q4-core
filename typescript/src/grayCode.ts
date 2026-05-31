/**
 * Gray-Code utilities for Q4 state transitions.
 *
 * Core invariant:
 *   hammingDistance(gray(n), gray(n+1)) === 1  for all n in 0..14
 */

/** Binary to Gray encoding: g(n) = n XOR (n >> 1). */
export const gray = (n: number): number => n ^ (n >> 1);

/** Gray to binary (inverse Gray-Code). */
export function ungray(g: number): number {
  let n = g;
  let mask = g >> 1;
  while (mask) {
    n ^= mask;
    mask >>= 1;
  }
  return n;
}

/** Number of differing bits between two integers. */
export function hammingDistance(a: number, b: number): number {
  let x = a ^ b;
  let count = 0;
  while (x) {
    count += x & 1;
    x >>= 1;
  }
  return count;
}

/**
 * Canonical Gray-Code traversal order of all 16 states.
 * Adjacent entries differ by exactly 1 bit.
 */
export const GRAY_ORDER: readonly number[] = [
  0, 1, 3, 2, 6, 7, 5, 4, 12, 13, 15, 14, 10, 11, 9, 8,
];

/** Return all state IDs reachable in exactly one Gray step from stateId. */
export function grayNeighbors(stateId: number): number[] {
  const g = gray(stateId);
  const result: number[] = [];
  for (let bit = 0; bit < 4; bit++) {
    const ng = g ^ (1 << bit);
    if (ng >= 0 && ng <= 15) result.push(ungray(ng));
  }
  return result.sort((a, b) => a - b);
}

/** True if the transition from→to is a valid single Gray-Code step. */
export function isValidTransition(from: number, to: number): boolean {
  return hammingDistance(gray(from), gray(to)) === 1;
}
