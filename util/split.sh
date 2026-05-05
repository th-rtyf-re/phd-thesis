#!/bin/sh

# Script for splitting the output pdf into the parts that US-AB will use to
# print.

SOURCE="../thesis-main.pdf"
OUT_PREFIX="split/Isaac-Ren-thesis-"
OUT_SUFFIX="-v1.pdf"

cpdf ${SOURCE} 3-90 -o ${OUT_PREFIX}Kappa${OUT_SUFFIX}
cpdf ${SOURCE} 93-138 -o ${OUT_PREFIX}Paper-A${OUT_SUFFIX}
cpdf ${SOURCE} 141-198 -o ${OUT_PREFIX}Paper-B${OUT_SUFFIX}
cpdf ${SOURCE} 201-242 -o ${OUT_PREFIX}Paper-C${OUT_SUFFIX}
cpdf ${SOURCE} 245-300 -o ${OUT_PREFIX}Paper-D${OUT_SUFFIX}
cpdf ${SOURCE} 303-end -o ${OUT_PREFIX}Paper-E${OUT_SUFFIX}
cpdf ${SOURCE} 91-92,139-140,199-200,243-244,301-302 -o ${OUT_PREFIX}Dividers${OUT_SUFFIX}