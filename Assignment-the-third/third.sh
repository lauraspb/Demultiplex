#!/usr/bin/bash
#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --cpus-per-task=8
#SBATCH --time=10:00:00
#SBATCH --mail-user='lpaez@uoregon.edu'
#SBATCH --mail-type=END,FAIL

/usr/bin/time -v python third.py \
-b /projects/bgmp/shared/2017_sequencing/indexes.txt \
-q 35 \
-r1 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz \
-r2 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz \
-i1 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz \
-i2 /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz


# -r1 /projects/bgmp/lpaez/bioinformatics/Bi622/Demultiplex/TEST-input_FASTQ/read1.fastq \
# -r2 /projects/bgmp/lpaez/bioinformatics/Bi622/Demultiplex/TEST-input_FASTQ/read2.fastq \
# -i1 /projects/bgmp/lpaez/bioinformatics/Bi622/Demultiplex/TEST-input_FASTQ/index1.fastq \
# -i2 /projects/bgmp/lpaez/bioinformatics/Bi622/Demultiplex/TEST-input_FASTQ/index2.fastq \
