#%%
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

#%%
label = sys.argv[1]
dirs = sys.argv[2:]
dirs.sort()

#%%
if not os.path.exists("figures"):
    os.mkdir("figures")

if not os.path.exists("summary_files"):
    os.mkdir("summary_files")

#%%
print("Initialize variables....")
N = len(dirs)
tmp = np.loadtxt(f"{label}/{dirs[0]}/summary_files/resample_times.txt")
T = tmp.shape[0]

resample_times = np.empty((N, T))
log_likelihoods = np.empty((N, T+1))

letter_ARIs = np.empty((N, T))
letter_macro_f1_scores = np.empty((N, T))
letter_micro_f1_scores = np.empty((N, T))

word_ARIs = np.empty((N, T))
word_macro_f1_scores = np.empty((N, T))
word_micro_f1_scores = np.empty((N, T))


print("Done!")

#%%
print("Loading results....")
for i, path in enumerate(dirs):
    resample_times[i] = np.loadtxt(f"{label}/{path}/summary_files/resample_times.txt")
    log_likelihoods[i] = np.loadtxt(f"{label}/{path}/summary_files/log_likelihood.txt")
    letter_ARIs[i] = np.loadtxt(f"{label}/{path}/summary_files/Letter_ARI.txt")
    letter_macro_f1_scores[i] = np.loadtxt(f"{label}/{path}/summary_files/Letter_macro_F1_score.txt")
    letter_micro_f1_scores[i] = np.loadtxt(f"{label}/{path}/summary_files/Letter_micro_F1_score.txt")
    word_ARIs[i] = np.loadtxt(f"{label}/{path}/summary_files/Word_ARI.txt")
    word_macro_f1_scores[i] = np.loadtxt(f"{label}/{path}/summary_files/Word_macro_F1_score.txt")
    word_micro_f1_scores[i] = np.loadtxt(f"{label}/{path}/summary_files/Word_micro_F1_score.txt")

print("Done!")

#%%
print("Ploting...")
plt.clf()
plt.errorbar(range(T), resample_times.mean(axis=0), yerr=resample_times.std(axis=0))
plt.xlabel("Iteration")
plt.ylabel("Execution time [sec]")
plt.title("Transitions of the execution time")
plt.savefig("figures/summary_of_execution_time.png")

plt.clf()
plt.errorbar(range(T+1), log_likelihoods.mean(axis=0), yerr=log_likelihoods.std(axis=0))
plt.xlabel("Iteration")
plt.ylabel("Log likelihood")
plt.title("Transitions of the log likelihood")
plt.savefig("figures/summary_of_log_likelihood.png")

plt.clf()
plt.errorbar(range(T), word_ARIs.mean(axis=0), yerr=word_ARIs.std(axis=0), label="Word ARI")
plt.errorbar(range(T), letter_ARIs.mean(axis=0), yerr=letter_ARIs.std(axis=0), label="Letter ARI")
plt.xlabel("Iteration")
plt.ylabel("ARI")
plt.title("Transitions of the ARI")
plt.legend()
plt.savefig("figures/summary_of_ARI.png")

plt.clf()
plt.errorbar(range(T), word_macro_f1_scores.mean(axis=0), yerr=word_macro_f1_scores.std(axis=0), label="Word macro F1")
plt.errorbar(range(T), letter_macro_f1_scores.mean(axis=0), yerr=letter_macro_f1_scores.std(axis=0), label="Letter macro F1")
plt.xlabel("Iteration")
plt.ylabel("Macro F1 score")
plt.title("Transitions of the macro F1 score")
plt.legend()
plt.savefig("figures/summary_of_macro_F1_score.png")

plt.clf()
plt.errorbar(range(T), word_micro_f1_scores.mean(axis=0), yerr=word_micro_f1_scores.std(axis=0), label="Word micro F1")
plt.errorbar(range(T), letter_micro_f1_scores.mean(axis=0), yerr=letter_micro_f1_scores.std(axis=0), label="Letter micro F1")
plt.xlabel("Iteration")
plt.ylabel("Micro F1 score")
plt.title("Transitions of the micro F1 score")
plt.legend()
plt.savefig("figures/summary_of_micro_F1_score.png")

plt.clf()
ll = log_likelihoods[:, -1]
lARI = letter_ARIs[:, -1]
wARI = word_ARIs[:, -1]
letter_slope, letter_intercept, letter_r_value, _, _ = stats.linregress(ll, lARI)
word_slope, word_intercept, word_r_value, _, _ = stats.linregress(ll, wARI)
plt.plot(ll, lARI, ".", color="tab:orange")
plt.plot(ll, wARI, ".", color="tab:blue")
left, right = plt.xlim()
left_and_right = np.array([left, right])
plt.plot(left_and_right, left_and_right*letter_slope+letter_intercept, "--", color="tab:orange", label=f"letter correlation:{letter_r_value:.3f}")
plt.plot(left_and_right, left_and_right*word_slope+word_intercept, "--", color="tab:blue", label=f"word correlation:{word_r_value:.3f}")
plt.xlabel("Log-likelihood")
plt.ylabel("Adjusted Rand index")
plt.title("Correlation between log-likelihood and ARI")
plt.legend()
plt.savefig("figures/correlation.png")
print("Done!")

#%%
print("Save npy files...")
np.save("summary_files/resample_times.npy", resample_times)
np.save("summary_files/log_likelihoods.npy", log_likelihoods)

np.save("summary_files/letter_ARI.npy", letter_ARIs)
np.save("summary_files/letter_macro_F1.npy", letter_macro_f1_scores)
np.save("summary_files/letter_micro_F1.npy", letter_micro_f1_scores)
np.save("summary_files/word_ARI.npy", word_ARIs)
np.save("summary_files/word_macro_F1.npy", word_macro_f1_scores)
np.save("summary_files/word_micro_F1.npy", word_micro_f1_scores)
print("Done!")
