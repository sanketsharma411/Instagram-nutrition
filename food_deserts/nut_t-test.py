# Loading stuff across all the
#path = 'C:\Users\Shweta\Desktop\CS 8903\FINAL/food_deserts\data\\'
path = '/nethome/ssharma321/FINAL/food_deserts/data'
file_fd ='/post_fd.txt'
file_nfd = '/post_nfd.txt'

from scipy import stats


with open(path+file_fd,'r') as f:
    fd_lines = f.readlines()
fd_lines = [line.strip().split('\t') for line in fd_lines]
cal_fd = [float(line[8]) for line in fd_lines]
sug_fd = [float(line[9]) for line in fd_lines]
fat_fd = [float(line[10]) for line in fd_lines]
cho_fd = [float(line[11]) for line in fd_lines]
fib_fd = [float(line[12]) for line in fd_lines]
pro_fd = [float(line[13]) for line in fd_lines]


with open(path+file_nfd,'r') as f:
    nfd_lines = f.readlines()
nfd_lines = [line.strip().split('\t') for line in nfd_lines]
cal_nfd = [float(line[8]) for line in nfd_lines]
sug_nfd = [float(line[9]) for line in nfd_lines]
fat_nfd = [float(line[10]) for line in nfd_lines]
cho_nfd = [float(line[11]) for line in nfd_lines]
fib_nfd = [float(line[12]) for line in nfd_lines]
pro_nfd = [float(line[13]) for line in nfd_lines]


with open('t-test_res','w+') as f:

	# assuming unequal population variances
	two_sample_diff_var = stats.ttest_ind(cal_fd, cal_nf, equal_var=False);	print " Calories t : %.3f  p : %.3f." % two_sample_diff_var
	f.write("  t : %.3f  p : %.3f \n" % two_sample_diff_var)

	# assuming unequal population variances
	two_sample_diff_var = stats.ttest_ind(sug_fd, sug_nf, equal_var=False);	print " Sugar t : %.3f  p : %.3f." % two_sample_diff_var
	f.write(" Sugar t : %.3f  p : %.3f \n" % two_sample_diff_var)

	# assuming unequal population variances
	two_sample_diff_var = stats.ttest_ind(fat_fd, fat_nf, equal_var=False);	print " Fat t : %.3f  p : %.3f." % two_sample_diff_var
	f.write(" Fat t : %.3f  p : %.3f \n" % two_sample_diff_var)

	# assuming unequal population variances
	two_sample_diff_var = stats.ttest_ind(cho_fd, cho_nf, equal_var=False);	print " Cholesterol t : %.3f  p : %.3f." % two_sample_diff_var
	f.write(" Cholesterol t : %.3f  p : %.3f \n" % two_sample_diff_var)

	# assuming unequal population variances
	two_sample_diff_var = stats.ttest_ind(fib_fd, fib_nf, equal_var=False);	print " Fiber t : %.3f  p : %.3f." % two_sample_diff_var
	f.write(" Fiber t : %.3f  p : %.3f \n" % two_sample_diff_var)

	# assuming unequal population variances
	two_sample_diff_var = stats.ttest_ind(pro_fd, pro_nf, equal_var=False);	print " Protein t : %.3f  p : %.3f." % two_sample_diff_var
	f.write(" Protein t : %.3f  p : %.3f \n" % two_sample_diff_var)
