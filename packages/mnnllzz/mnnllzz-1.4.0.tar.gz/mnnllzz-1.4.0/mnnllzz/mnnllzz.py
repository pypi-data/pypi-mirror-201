#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import shutil
import glob
import re
import string
import json
from subprocess import PIPE, run

import random
from decimal import Decimal
import numpy as np
import scipy.optimize
# from numpy import sqrt, exp, sin, cos, tan, log, log10, pi, floor, abs

np.seterr(all="raise")  # https://stackoverflow.com/questions/15933741

#%% Class definition.

class RandomSearchStuck(Exception):
    def __init__(self, msg):
        self.msg = msg


class RangeBoundaryExceeded(Exception):
    def __init__(self, msg):
        self.msg = msg


class ExamTest():

    def __init__(self,
                 template_text, testnr,
                 solutions,
                 test_name, year, month, day,
                 salt_1, salt_2,
                 mark_sol=False):
        # A string containing the whole TeX template.
        self.source_text = template_text
        # The number of this test.
        self.testnr = testnr
        # List of lists of dictionaries with the solutions.
        self.solutions = solutions
        # Name of the test.  Some checks on the format.
        ww = test_name.replace("_", " ").split()  # from underscore to spaces
        for iw,w in enumerate(ww):
            if (len(w) > 3):    # capitalize first letter of long words
                ww[iw] = w[0].upper() + w[1:]
        self.test_name = " ".join(ww)
        # The date.
        self.test_year = year
        self.test_month = month
        self.test_day = day
        # Whether to mark correct solutions.
        self.mark_sol = mark_sol
        # Set seeds for the random numbers based on the test number.
        random.seed(salt_1 * (testnr + 1))  # for the letters
        np.random.seed(salt_2 * (testnr + 1))   # for the values
        # Constant: uppercase alphabet.
        self._letters = string.ascii_uppercase
        # Mathematical functions for the evaluation of formulas.
        self.mfe = {
            "sqrt": np.sqrt, "exp": np.exp, "sin": np.sin, "cos": np.cos,
            "tan": np.tan, "log": np.log, "log10": np.log10, "pi": np.pi,
            "floor": np.floor, "ceil": np.ceil, "round": np.round, "abs": np.abs,
            "bisect": scipy.optimize.bisect}


    def apply_subst(self):
        # Check that no key in the substitution dictionary matches another one.
        # For example, the key "MASS" matches "MASS1", which would produce an
        # erroneous expression in the text after substitution.
        keys_OK = True
        keys_list = list(self.subst.keys())
        for key in keys_list:
            for key1 in keys_list:
                if (key != key1):  # it is the same key if the strings are equal
                    if (key in key1):
                        print("CONFUSING LABELS: %s matches %s." % (key, key1))
                        keys_OK = False
                        break  # break from inner loop
            if (not keys_OK):
                break  # break from outer loop

        if keys_OK:
            # Create a regular expression  from the dictionary keys
            all_labels = re.compile("(%s)" % "|".join(map(re.escape, self.subst.keys())))
            # For each match, look-up corresponding value in dictionary
            self.source_text = all_labels.sub(
                lambda mo: self.subst[mo.string[mo.start():mo.end()]], self.source_text)


    def fexp(self, number):
        # Calculate the exponent of a number, base 10.
        (sign, digits, exponent) = Decimal(number).as_tuple()
        r = len(digits) + exponent - 1
        return r


    def fman(self, number):
        # Calculate the mantissa of a number, base 10.
        r = Decimal(number).scaleb(-self.fexp(number)).normalize()
        return r


    def number_format(self, val):
        # Format a number in different ways based on its length.
        # Always use 3 significant digits.
        m = self.fman(val)  # mantissa
        e = self.fexp(val)  # exponent
        if (e == 0):  # 1.23
            r = r"\ensuremath{%.2f}" % val
        elif (e == 1):  # 12.3
            r = r"\ensuremath{%.1f}" % val
        elif (e == 2):  # 123
            r = r"\ensuremath{%.0f}" % val
        elif (e == -1):  # 0.123
            r = r"\ensuremath{%.3f}" % val
        elif (e == -2):  # 0.0123
            r = r"\ensuremath{%.4f}" % val
        else:
            r = r"\ensuremath{%.2f \times 10^{%d}}" % (m, e)
        return r


    def eval_check(self, str_expr):
        # Execute an expression with a custom set of globals and checks.
        x = self.x
        c = self.c
        try:
            r = eval(str_expr, {**self.c, **self.x, **self.mfe})
        except (RuntimeWarning, OverflowError, ValueError, FloatingPointError):
            print("\n\nError evaluating: %s" % str_expr)
            sys.exit("Stop.")
        return r


    def const_set(self, name, label, val):
        # Save the value to the dictionary of values.
        self.c[name] = val
        # Save the replacement to be made in the template.
        self.subst[label] = self.number_format(val)


    def trn(self, val, dig=3, upwards=False):
        # Truncate number to num significat digits.
        m = float(self.fman(val))  # mantissa
        e = float(self.fexp(val))  # exponent
        if upwards:  # truncate up
            m = int(m * 10.0**(dig-1.0) + 1) / 10.0**(dig-1.0)
        else:  # truncate down
            m = int(m * 10.0**(dig-1.0)) / 10.0**(dig-1.0)
        r = m * 10.0**e
        return r


    def param_set(self, name, label, valmin, valmax):
        # Calculate a random value for the parameter.
        valmax_trn = self.trn(0.9999 * valmax, dig=2)
        valmin_trn = self.trn(1.0001 * valmin, dig=2, upwards=True)
        val = self.trn(np.random.uniform(valmin_trn, valmax_trn), dig=2)
        if (val < valmin or val > valmax):
            data = (("\033[1;31mError: Range exceeded in param_set for parameter %s\n"
                    + "It might be that the range is too narrow to truncate the values to 2 digits.\033[0;0m\n"
                    + "Min: %e, Min Trunc: %e\nMax: %e, Max Trunc: %e\nVal: %e")
                    % (name, valmin, valmin_trn, valmax, valmax_trn, val))
            raise RangeBoundaryExceeded(data)
        # Save the value to the dictionary of values.
        self.x[name] = val
        # Save the replacement to be made in the template.
        self.subst[label] = self.number_format(val)
        return val


    def random_options(self, valpres, label_question, num=5,
                       val_range=None, exp_range_width=None):
        # Choose num values uniformly distributed between valmin and valmax.
        # Reject values which are too close to each other or the solution.
        # List containing the values, including the solution as first element.
        valsol = valpres[0]
        vv = valpres.copy()
        # Decide which random distribution to use.
        if (val_range is not None):
            distro = "uniform"
        elif (exp_range_width is not None):
            distro = "log"

        # Calculate range of random options.
        if (distro == "uniform"):
            valmin = val_range[0]
            valmax = val_range[1]
        elif (distro == "log"):
            exp_max = np.random.uniform(0.2, exp_range_width)
            exp_min = exp_max - exp_range_width
            val_1 = valsol * (10.0 ** exp_min)
            val_2 = valsol * (10.0 ** exp_max)
            valmin = np.minimum(val_1, val_2)
            valmax = np.maximum(val_1, val_2)

        # The minimum acceptable relative difference between two values.
        if (distro == "uniform"):
            delta = np.abs((valmax - valmin) / (2 * num) / valmax)
        else:
            delta = 0.05

        i_try = 0
        v_try_hist = []
        while (len(vv) < num):
            # Randomly choose a new value.
            if (distro == "uniform"):
                v_try = np.random.uniform(valmin, valmax)
            elif (distro == "log"):
                exp_try = np.random.uniform(exp_min, exp_max)
                v_try = valsol * (10.0 ** exp_try)
            v_try_hist.append(np.sort(vv + [valmin,valmax,v_try]))
            # The minimum difference with the accepted values so far.
            epsilon = np.array([np.abs((v_try - v) / np.maximum(v_try, v)) for v in vv]).min()
            if (epsilon > delta):
                vv.append(v_try)
            i_try = i_try + 1
            # Prevent loop being stuck.
            if (i_try > 100):
                data = ("\033[1;31mError: Loop stuck in random_options for question %s\033[0;0m\n"
                        + "Sol: %e, Min: %e, Max: %e\n") % (label_question, valsol, valmin, valmax)
                for t in v_try_hist:
                    data = data + "\n" + " ".join("%.2e" % x for x in t)
                raise RandomSearchStuck(data)
        # Return the new values only as an array.
        rr = np.array(vv[len(valpres):])
        return rr


    def solution_set(self, label_question, x_sol,
                     x_forced=None, keep_sign=True, x_range=None, num=5):

        # Initialize the values of the option and the respective indices,
        # and then reshuffle the lists.
        
        # The correct solution.
        vv = [x_sol]

        # The forced option(s).
        if (x_forced is not None):
            # Be sure to have a list of values.
            if not isinstance(x_forced, list):
                x_forced_vals = [x_forced,]
            else:
                x_forced_vals = x_forced
            # Iterate over the forced value(s) if there are choices.
            for x_val in x_forced_vals:
                if len(vv) < num:
                    vv.append(x_val)


        # Correct solution and non-string forced option(s).
        vv_f = [v for v in vv if not isinstance(v, str)]
        num_str = len(vv) - len(vv_f)  # how many strings among forced
        num_rand = num - num_str  # how many new random numerical options we need

        # Calculate random values for the remaining choices.
        try:
            if (x_range is not None):
                rr = self.random_options(vv_f, label_question, num=num_rand,
                                         val_range=[x_range[0], x_range[1]])
            elif (keep_sign):
                rr = self.random_options(vv_f, label_question, num=num_rand,
                                         exp_range_width=0.7)
            else:
                rr = self.random_options(vv_f, label_question, num=num_rand,
                                         exp_range_width=0.7)
                # Randomize signs.
                # Start from one plus and one minus for each option, and then
                # add the opposite sign of the correct solution.  Then
                # randomize all signs.
                ss = [1.0,-1.0] * len(rr) + [-np.sign(x_sol)]
                random.shuffle(ss)
                for i in range(len(rr)):  # multiply by the random signs
                    rr[i] = rr[i] * ss[i]
            # Append to the list of choice values and indices.
            for r in rr:
                vv.append(r)
        except (RuntimeWarning, OverflowError):
            print("Error in random options of solution %s" % label_question)
            print("%e" % (x_sol))
            sys.exit("Stop.")

        # Shuffle the options and save the new index of the correct solution.
        if len(vv) != num:
            print("Error in preparing options of solution %s" % label_question)
            print("%d" % len(vv))
            sys.exit("Stop.")
        ii = list(range(num))
        random.shuffle(ii)
        xx = [None] * num
        for i,v in zip(ii,vv):
            xx[i] = v
        i_sol = ii[0]
        
        # Save the solution to an instance list.
        self.sol_values.append(x_sol)
        # TODO: now solutions are supposed to be numbers, because of how we
        # deal with sol_values later on in the code.
        # Strings are allowed as forced answers, but not as the correct value.
        # The problem is how to handle the TSV file with the numerical values.
        # Either we produce a file which is mixed numbers and string (find the
        # correct format for Excel... but look out for TeX symbols) or hash
        # the string into a number using e.g.: hash(string) % (10**8).       
        self.sol_letters.append(self._letters[i_sol])

        # Save the replacements to be made in the template.
        for i_opt,(val,a) in enumerate(zip(xx,self._letters[:num])):
            # The string for this replacement.
            if isinstance(val, str):
                repl_val = val  # already a string
            else:
                repl_val = self.number_format(val)  # format number
            # The label for this replacement.
            if ((i_opt == i_sol) and self.mark_sol):
                # Replace the box to mark the solution as correct.
                label_choice = r"%s \fbox{%s%s}" % (a,label_question,a)
                subst_choice = r"\parbox[t]{2cm}{%s \fbox{%s}}\hspace{-2cm}\parbox{2cm}{\bf \Large \hspace{-7pt} \raisebox{1pt}{X}}\hspace{-2cm}\phantom{%s \fbox{%s}}" % (
                    a, repl_val, a, repl_val)
            else:
                # Just replace the number.
                label_choice = label_question + a
                subst_choice = repl_val
            # The replacement.
            self.subst[label_choice] = subst_choice


    def values_def(self):

        # Iterate over several trials to satisfy constraints on the output.
        values_found = False
        n_try = 0
        while(not values_found):
            n_try = n_try + 1

            # The literal substitutions to be made in the TeX template.
            self.subst = {}
            self.subst["TESTNR"] = "%d" % self.testnr
            self.subst["TESTNAME"] = self.test_name
            self.subst["ANNO"] = "%04d" % self.test_year
            self.subst["MESE"] = "%02d" % self.test_month
            self.subst["GIORNO"] = "%02d" % self.test_day
            # The constants in the problems.
            self.c = {}
            # Truth values for the constraints.
            self.constraints = []
            # The letters of the solution.
            self.sol_letters = []
            # The values of the solution.
            self.sol_values = []

            # A list of all constants, parameters, variables, and solutions.
            self.dump_names = []
            self.dump_values = []

            # Read the JSON with the values of the parameters to fill in.
            for sol_block in self.solutions:
                # The variables in the current problem.
                self.x = {}
                for op in sol_block:
                    # Constant with a fixed value.
                    if (op["type"] == "constant"):
                        val = self.eval_check(op["value"])
                        self.const_set(op["name"], op["label"], val)
                        # Dump.
                        self.dump_names.append(op["name"])
                        self.dump_values.append(val)
                    # Parameter, with a randomly chosen value.
                    elif (op["type"] == "parameter"):
                        valmin = self.eval_check(op["min"])
                        valmax = self.eval_check(op["max"])
                        val = self.param_set(op["name"], op["label"], valmin, valmax)
                        # Dump.
                        self.dump_names.append(op["name"])
                        self.dump_values.append(val)
                    # Generic variable needed to calculate the solution.
                    elif (op["type"] == "variable"):
                        val = self.eval_check(op["value"])
                        self.x[op["name"]] = val
                        # Dump.
                        self.dump_names.append(op["name"])
                        self.dump_values.append(val)
                    # Value of the solution, with optional parameters to
                    # determine the set of multiple choices.
                    elif (op["type"] == "solution"):
                        # Check which optional parameters are set in the JSON
                        # end evaluate their values.
                        opt_keys = ["x_forced", "keep_sign", "x_range"]
                        opt_dict = {}
                        for k in opt_keys:
                            if k in op:
                                val = self.eval_check(op[k])
                                opt_dict[k] = val
                        # Set the value of the solution and pass optional
                        # arguments to the function.
                        val = self.eval_check(op["value"])
                        self.solution_set(op["label"], val, **opt_dict)
                        # Dump.
                        self.dump_names.append(op["label"])
                        self.dump_values.append(val)
                    elif (op["type"] == "constraint"):
                        val = self.eval_check(op["condition"])
                        self.constraints.append(val)

            # If we satisfy all constraint, exit the loop and save the dict of
            # substitutions and the lists of solutions.
            if (all(self.constraints)):
                values_found = True
                # Print if this is not the first try.
                if (n_try > 1):
                    print("%03d \033[0;32mConstraints fulfilled after %d tries.\033[0;0m" % (self.testnr, n_try))
            else:
                # Stop the loop anyway.
                if (n_try > 19):
                    print("%03d \033[1;31mConstraints not fulfilled.\033[0;0m" % self.testnr)
                    self.subst = {}
                    self.subst["TESTNR"] = "TESTO NON VALIDO"
                    break


#%% Definition of typesetting procedure.

def update_progress(progress):
    # https://stackoverflow.com/questions/3160699/python-progress-bar
    barLength = 20
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "Error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rTypesetting: [{0}] {1:3.0f}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()


def typeset_tests(p, template_text):

    # Read the template.
    # with open(p["template_filename"], "r") as f:
    #     template_text = f.read()

    # Prepare directories for the build.
    if os.path.exists("build") and os.path.isdir("build"):
        shutil.rmtree("build")
    if os.path.exists("distribute") and os.path.isdir("distribute"):
        shutil.rmtree("distribute")
    os.mkdir("build")
    os.mkdir("distribute")
    for filename in glob.glob("*.png"):
        shutil.copy(filename, "build")

    gen_err = False  # error in the calculations

    # Produce test with correct solutions marked.
    # Also useful for debugging calculations.
    if (p["solution_test"]):

        # Create a test instance, based on the template.
        test_data = ExamTest(
            template_text, 0, p["solutions"],
            p["test_name"], p["test_year"], p["test_month"], p["test_day"],
            p["random_salt_1"], p["random_salt_2"],
            mark_sol=True)

        try:
            # Calculate random parameters and solutions.
            test_data.values_def()
        except (RandomSearchStuck, RangeBoundaryExceeded) as err:
            print(err.msg)
            gen_err = True

        if (gen_err or p["values_only"]):
            # Dump values.
            print("Dump of Solution Test:")
            for n,v in zip(test_data.dump_names, test_data.dump_values):
                print("%s %15.8e" % ((n+" ").ljust(15,"."),v))            
        else:
            # Substitute the random values into the template.
            test_data.apply_subst()

            # Save the complete source TeX file.
            with open("build/temp.tex", "w") as f:
                f.write(test_data.source_text)

            # Compile the source TeX and move the PDF to a different folder.
            test_name = p["test_name"].replace(" ", "_").lower()
            pdfname = "%04d-%02d-%02d_%s" % (
                p["test_year"], p["test_month"], p["test_day"], test_name)
            os.chdir("build")
            # os.system(f"pdflatex -quiet -jobname={pdfname} temp.tex")
            # os.system(f"pdflatex --interaction=batchmode -jobname={pdfname} temp.tex")
            r = run(f"pdflatex --interaction=batchmode -jobname={pdfname} temp.tex", stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
            os.chdir("..")
            shutil.copy(os.path.join("build", f"{pdfname}.pdf"), ".")

    # Produce all the standard tests.  Save solutions to lists.
    if (not gen_err and p["num_tests"] > 0):
        # Data to be saved for each test successfully generated.
        sol_letters = []
        sol_values = []
        dump_names = []
        dump_tests = []

        # Iterate over the tests.
        for i_test in np.arange(p["num_tests"]):

            # Create a test instance, based on the template.
            test_data = ExamTest(
                template_text, i_test + 1, p["solutions"],
                p["test_year"], p["test_month"], p["test_day"],
                p["random_salt_1"], p["random_salt_2"],
                mark_sol=False)

            try:
                # Calculate random parameters and solutions.
                test_data.values_def()
            except (RandomSearchStuck, RangeBoundaryExceeded) as err:
                update_progress(-1.0)
                # print("ERROR: Cannot find random values for test %d." % i_test)
                print(err.msg)
                gen_err = True
                # Dump values.
                print("Dump of Test %d" % (i_test + 1))
                for n,v in zip(test_data.dump_names, test_data.dump_values):
                    print("%s %15.8e" % ((n+" ").ljust(15,"."),v))           
                break

            # Save test data.
            sol_letters.append(test_data.sol_letters)
            sol_values.append(test_data.sol_values)
            if (len(dump_names) == 0):  # save only once, they are all equal
                dump_names = test_data.dump_names.copy()
            dump_tests.append(test_data.dump_values.copy())

            if (not p["values_only"]):
                # Substitute the random values into the template.
                test_data.apply_subst()

                # Save the complete source TeX file.
                with open(os.path.join("build","temp.tex"), "w") as f:
                    f.write(test_data.source_text)

                # Compile the source TeX and move the PDF to a different folder.
                pdfname = "compito_%03d" % test_data.testnr
                os.chdir("build")
                # os.system(f"pdflatex -quiet -jobname={pdfname} temp.tex")
                # os.system(f"pdflatex --interaction=batchmode -jobname={pdfname} temp.tex")
                r = run(f"pdflatex --interaction=batchmode -jobname={pdfname} temp.tex", stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
                os.chdir("..")
                shutil.copy(os.path.join("build", f"{pdfname}.pdf"), "distribute")

                update_progress((i_test + 1.0)/p["num_tests"])


    if (not gen_err and p["num_tests"] > 0):
        # Save dump values for all the tests.   
        with open("dump_values.tsv", "w") as f:
                f.write("testnr\t" + "\t".join(dump_names) + "\n")
                for i_test,dump_values in enumerate(dump_tests):
                    f.write(("%d\t" % (i_test+1)) + "\t".join([("%15.8e" % v) for v in dump_values]) + "\n")
        if (not p["values_only"]): 
            # Save the letters and the values of the solution.
            # Each row correspond to a test, each column to a question.
            # Use TSV, which makes it easier to copy-paste to a web-based spreadsheet.
            with open(os.path.join("distribute","solution_letters.tsv"), "w") as f:
                    f.write("\n".join(["\t".join(letters) for letters in sol_letters]))

            with open(os.path.join("distribute","solution_numbers.tsv"), "w") as f:
                    f.write("\n".join(["\t".join(map(lambda x: "%.4E" % x, values)) for values in sol_values]))

    if (not gen_err):
        print("\033[1;32m\nGeneration succeeded.\033[0;0m\n")
    else:
        print("\033[1;31m\nGeneration failed.\033[0;0m\n")

    # Clean the build folder.
    if os.path.exists("build") and os.path.isdir("build"):
        shutil.rmtree("build")

