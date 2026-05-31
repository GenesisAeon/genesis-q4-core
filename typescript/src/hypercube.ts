/**
 * 4D Hypercube (Tesseract) topology for the Q4 state space.
 *
 * Topology:
 *   Vertices: 16   (= 16 Q4 states)
 *   Edges:    32   (= valid 1-bit transitions)
 *   Faces:    24   (= 2-bit similarity groups)
 *   Cells:     8   (= 3-bit subspaces)
 *
 * Mathematical graph structure — not a metaphysical claim.
 */

import { gray, ungray, hammingDistance, grayNeighbors } from "./grayCode";
import { q4StateFromId, Q4StateFull } from "./Q4State";

export interface TesseractEdge {
  from: number;
  to: number;
}

export class Tesseract {
  readonly vertices = 16;
  readonly edges = 32;
  readonly faces = 24;
  readonly cells = 8;

  private readonly adj: Map<number, number[]>;

  constructor() {
    this.adj = new Map();
    for (let i = 0; i < 16; i++) {
      this.adj.set(i, grayNeighbors(i));
    }
  }

  neighbors(stateId: number): number[] {
    return [...(this.adj.get(stateId) ?? [])];
  }

  neighborsAsStates(stateId: number): Q4StateFull[] {
    return this.neighbors(stateId).map(q4StateFromId);
  }

  areAdjacent(a: number, b: number): boolean {
    return (this.adj.get(a) ?? []).includes(b);
  }

  /** BFS shortest path from→to. Returns state IDs inclusive. */
  shortestGrayPath(from: number, to: number): number[] {
    if (from === to) return [from];
    const prev = new Map<number, number | null>([[from, null]]);
    const queue = [from];
    let head = 0;
    while (head < queue.length) {
      const cur = queue[head++];
      for (const nb of this.neighbors(cur)) {
        if (!prev.has(nb)) {
          prev.set(nb, cur);
          if (nb === to) return this._reconstruct(prev, from, to);
          queue.push(nb);
        }
      }
    }
    throw new Error(`No path from ${from} to ${to}`);
  }

  private _reconstruct(prev: Map<number, number | null>, _from: number, to: number): number[] {
    const path: number[] = [];
    let cur: number | null = to;
    while (cur !== null) {
      path.push(cur);
      cur = prev.get(cur) ?? null;
    }
    return path.reverse();
  }

  allEdges(): TesseractEdge[] {
    const seen = new Set<string>();
    const result: TesseractEdge[] = [];
    for (const [a, nbs] of this.adj) {
      for (const b of nbs) {
        const key = `${Math.min(a, b)}-${Math.max(a, b)}`;
        if (!seen.has(key)) {
          seen.add(key);
          result.push({ from: Math.min(a, b), to: Math.max(a, b) });
        }
      }
    }
    return result.sort((a, b) => a.from - b.from || a.to - b.to);
  }
}
