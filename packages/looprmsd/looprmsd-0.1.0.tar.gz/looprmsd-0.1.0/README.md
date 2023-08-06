## Description
PDB 2개랑 loop_region 지정해주면 RMSD 구해주는 라이브러리

Input PDB 가 chothia numbering 이 아니면 anarci 로 chothia numbering 으로 변환해 RMSD 계산.
현재는 항체에 대해서만 RMSD 구해줌. (H1-H3, L1-L3)

H1: 26-35
H2: 50-65
H3: 95-102
L1: 24-34
L2: 50-56
L3: 89-97

## Requirements
```bash
anarci  # conda install anarci
biopython
numpy
```

## Example

1. Loop region 지정해주면 RMSD 구해줌.
```
from looprmsd import pdb_rmsd
rmsd = pdb_rmsd(model_pdb, ref_pdb, 'H', 'H', loop_region='H3')  #0.5385195760350145
```

2. Seq 주면 RMSD 구해줌.
```
from looprmsd import pdb_rmsd
rmsd = pdb_rmsd(model_pdb, ref_pdb, 'H', 'H', loop_seq='YPHYYGSSHWYFDV')  #0.5385195760350145
```

## Detail
1. Use Carbon Alpha only in RMSD calculation
2. Superposition is done by +-2 residue from given loop.


## TODO
general protein 까지 확장
    시나리오 : 
    AF 의 output 이든 (=seqres)
    unifold output 이든 (=chothia) 
    RMSD 구할 수 있도록 