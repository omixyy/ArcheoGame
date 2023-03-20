#include <stdio.h>
#include <stdlib.h>

float PlayerStatsFormula(float rt1, float rt2,
                         float kpr1, float kpr2,
                         float dpr1, float dpr2,
                         float hs1, float hs2){
    return (rt1 / (rt1 + rt2) +
            kpr1 / (kpr1 + kpr2) +
            (1 - dpr1 / (dpr1 + dpr2)) +
            hs1 / (hs1 + hs2)) * 25;
}

float TeamStatsFormula(int r1, int r2,
                       float av_rating1, float av_rating2,
                       int str1, int str2) {
    float* streak_prob = NULL;
    streak_prob = malloc(sizeof(float));
    float rank1 = (float)r1;
    float rank2 = (float)r2;
    float streak1 = (float)str1;
    float streak2 = (float)str2;
    if (streak_prob != NULL) {
        if (streak1 <= 8 && streak2 <= 8 && streak1 != 0 && streak2 != 0) *streak_prob = streak1 / (streak1 + streak2);
        else if (streak1 <= 8 && streak2 <= 8) *streak_prob = 0.5;
        else if (streak2 <= 8) *streak_prob = streak1 / (streak1 + streak2 + (streak1 - 8));
        else if (streak1 <= 8) *streak_prob = streak1 / (streak1 + streak2 - 8);
        else *streak_prob = 1 - streak1 / (streak1 + streak2);
    }
    float gen_probability = (1 - rank1 / (rank1 + rank2) + av_rating1 / (av_rating1 + av_rating2) + *streak_prob) * 33.33;
    free(streak_prob);
    return gen_probability;
}

int StatsCorrector(float stat, float new_stat,
                   float play_stat, int maps) {
    if (stat < play_stat && play_stat < new_stat) return 0;
    else if (stat > play_stat && play_stat > new_stat) return 0;
    else if (new_stat < play_stat && play_stat > play_stat) return 0;
    return (int)((maps * new_stat - maps * stat) / (play_stat - new_stat)) + 1;
}
