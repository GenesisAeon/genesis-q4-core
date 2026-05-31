/**
 * Q4State — 4-bit state in the GenesisAeon Q4 state space.
 *
 * 16 states = 4 bit. H = log2(16) = 4 bit. NOT 16 bit.
 */

export interface Q4StateData {
  C: 0 | 1;
  R: 0 | 1;
  E: 0 | 1;
  P: 0 | 1;
}

export interface Q4StateFull extends Q4StateData {
  readonly id: number;      // 0..15  (8*C + 4*R + 2*E + P)
  readonly binary: string;  // "0000".."1111"
  readonly grayId: number;  // Gray-encoded ID: id ^ (id >> 1)
  readonly entropyBits: number; // 4.0 at uniform distribution
}

/** Construct a full Q4State from flags. */
export function makeQ4State(C: 0|1, R: 0|1, E: 0|1, P: 0|1): Q4StateFull {
  const id = 8 * C + 4 * R + 2 * E + P;
  return {
    C, R, E, P,
    id,
    binary: id.toString(2).padStart(4, "0"),
    grayId: id ^ (id >> 1),
    entropyBits: 4.0,
  };
}

/** Construct a Q4State from its integer ID (0..15). */
export function q4StateFromId(id: number): Q4StateFull {
  if (id < 0 || id > 15) throw new RangeError(`state id must be 0..15, got ${id}`);
  return makeQ4State(
    ((id >> 3) & 1) as 0 | 1,
    ((id >> 2) & 1) as 0 | 1,
    ((id >> 1) & 1) as 0 | 1,
    (id & 1) as 0 | 1,
  );
}

/** All 16 Q4 states ordered by ID. */
export function allQ4States(): Q4StateFull[] {
  return Array.from({ length: 16 }, (_, i) => q4StateFromId(i));
}
