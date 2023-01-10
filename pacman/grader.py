# grading.py
# ----------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"Common code for autograders"

import html
import json
import time
import traceback
from collections import defaultdict
from typing import Callable
from typing import Dict
from typing import Hashable
from typing import List

import util


class Grader:
    "A data structure for name_project grader, along with formatting code to graphics_pacman them"

    def __init__(self,
                 name_project: str,
                 list_str_question,
                 bool_output_json: bool = False,
                 bool_output_html: bool = False,
                 bool_output_mute: bool = False):
        """
        Defines the grading scheme for a name_project
          name_project: name_project test_case_object
          questionsAndMaxesDict: a list of (str_question test_case_object, max points per str_question)
        """
        self.questions: List[str] = [el[0] for el in list_str_question]  # TODO: Example: ['q1']
        self.maxes: Dict = dict(list_str_question)
        self.points: Counter = Counter()
        self.messages: Dict = dict([(q, []) for q in self.questions])
        self.name_project: str = name_project
        self.start = time.localtime()[1:6]
        self.sane: bool = True  # Sanity checks
        self.currentQuestion = None  # Which str_question we're grading
        self.bool_output_html: bool = bool_output_html
        self.bool_output_json: bool = bool_output_json  # GradeScope output
        self.bool_output_mute: bool = bool_output_mute
        self.prereqs: Dict[Hashable, set] = defaultdict(set)

        # print 'Autograder transcript for %s' % self.name_project
        print('Starting on %d-%d at %d:%02d:%02d' % self.start)

    def addPrereq(self, name_question: str, prereq):
        raise Exception("addPrereq IS CALLED???? HOW IS THAT POSSIBLE")
        self.prereqs[name_question].add(prereq)

    def grade(self,
              dict_k_name_question_v_callable: Dict[str, Callable],
              exceptionMap={},
              bool_display_picture_bonus: bool = False
              ):
        """
        Grader each str_question
          dict_k_name_question_v_callable: the module with all the grading functions (pass in with sys.modules[__name__])
        """

        completedQuestions = set()

        # print("self.questions", self.questions)  # REMOVE ME PLS
        for q in self.questions:
            print('\nQuestion %s' % q)
            print('=' * (9 + len(q)))
            print()
            self.currentQuestion = q

            incompleted = self.prereqs[q].difference(completedQuestions)

            if len(incompleted) > 0:
                prereq = incompleted.pop()
                print("*** NOTE: Make sure to complete Question {} before working on Question {},\n "
                      "*** because Question {} builds upon your answer for Question {}.".format(prereq, q, q, prereq))
                continue

            if self.bool_output_mute:
                util.mutePrint()
            try:
                # Call the str_question's function
                # TimeoutFunction(getattr(dict_k_name_question_v_callable, q),1200)(self)

                # Call the str_question's function
                util.TimeoutFunction(dict_k_name_question_v_callable.get(q), 1800)(self)  # TODO: CHANGE THAT 1800 TO A CONST OR SOMESHIT

            except Exception as inst:
                self.addExceptionMessage(q, inst, traceback)
                self.addErrorHints(exceptionMap, inst, q[1])
            except:
                self.fail('FAIL: Terminated with a string exception.')
            finally:
                if self.bool_output_mute:
                    util.unmutePrint()

            if self.points[q] >= self.maxes[q]:
                completedQuestions.add(q)

            print('\n### Question %s: %d/%d ###\n' %
                  (q, self.points[q], self.maxes[q]))

        print('\nFinished at %d:%02d:%02d' % time.localtime()[3:6])
        print("\nProvisional grader\n==================")

        for q in self.questions:
            print('Question %s: %d/%d' % (q, self.points[q], self.maxes[q]))
        print('------------------')
        print('Total: %d/%d' %
              (self.points.totalCount(), sum(self.maxes.values())))
        if bool_display_picture_bonus and self.points.totalCount() == 25:
            print("""

                     ALL HAIL GRANDPAC.
              LONG LIVE THE GHOSTBUSTING KING.

                  ---      ----      ---
                  |  \    /  + \    /  |
                  | + \--/      \--/ + |
                  |   +     +          |
                  | +     +        +   |
                @@@@@@@@@@@@@@@@@@@@@@@@@@
              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            \   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
             \ /  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
              V   \   @@@@@@@@@@@@@@@@@@@@@@@@@@@@
                   \ /  @@@@@@@@@@@@@@@@@@@@@@@@@@
                    V     @@@@@@@@@@@@@@@@@@@@@@@@
                            @@@@@@@@@@@@@@@@@@@@@@
                    /\      @@@@@@@@@@@@@@@@@@@@@@
                   /  \  @@@@@@@@@@@@@@@@@@@@@@@@@
              /\  /    @@@@@@@@@@@@@@@@@@@@@@@@@@@
             /  \ @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            /    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
              @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                @@@@@@@@@@@@@@@@@@@@@@@@@@
                    @@@@@@@@@@@@@@@@@@

""")
        print(
            "Your grader are NOT yet registered. To register your grader, make sure to follow your instructor's guidelines to receive credit on your name_project."
        )

        print("self.prereqs", self.prereqs)


        if self.bool_output_html:
            self.produceOutput()
        if self.bool_output_json:
            self.produceGradeScopeOutput()

    def addExceptionMessage(self, q, inst, traceback):
        """
        Method to format the exception message, this is more complicated because
        we need to cgi.escape the traceback but wrap the exception in a <pre> tag
        """
        self.fail('FAIL: Exception raised: %s' % inst)
        self.addMessage('')
        for line in traceback.format_exc().split('\n'):
            self.addMessage(line)

    def addErrorHints(self, exceptionMap, errorInstance, questionNum):
        typeOf = str(type(errorInstance))
        questionName = 'q' + questionNum
        errorHint = ''

        # str_question specific error hints
        if exceptionMap.get(questionName):
            questionMap = exceptionMap.get(questionName)
            if (questionMap.get(typeOf)):
                errorHint = questionMap.get(typeOf)
        # fall back to general error messages if a str_question specific
        # one does not exist
        if (exceptionMap.get(typeOf)):
            errorHint = exceptionMap.get(typeOf)

        # dont include the HTML if we have no error hint
        if not errorHint:
            return ''

        for line in errorHint.split('\n'):
            self.addMessage(line)

    def produceGradeScopeOutput(self):
        out_dct = {}

        # total of entire submission
        total_possible = sum(self.maxes.values())
        total_score = sum(self.points.values())
        out_dct['score'] = total_score
        out_dct['max_score'] = total_possible
        out_dct['output'] = "Total score (%d / %d)" % (
            total_score, total_possible)

        # individual tests
        tests_out = []
        for name in self.questions:
            test_out = {}
            # test test_case_object
            test_out['test_case_object'] = name
            # test score
            test_out['score'] = self.points[name]
            test_out['max_score'] = self.maxes[name]
            # others
            is_correct = self.points[name] >= self.maxes[name]
            test_out['output'] = "  Question {num} ({points}/{max}) {correct}".format(
                num=(name[1] if len(name) == 2 else name),
                points=test_out['score'],
                max=test_out['max_score'],
                correct=('X' if not is_correct else ''),
            )
            test_out['tags'] = []
            tests_out.append(test_out)
        out_dct['tests'] = tests_out

        # file output
        with open('gradescope_response.json', 'w') as outfile:
            json.dump(out_dct, outfile)
        return

    def produceOutput(self):
        edxOutput = open('edx_response.html', 'w')
        edxOutput.write("<div>")

        # first sum
        total_possible = sum(self.maxes.values())
        total_score = sum(self.points.values())
        checkOrX = '<span class="incorrect"/>'
        if (total_score >= total_possible):
            checkOrX = '<span class="correct"/>'
        header = """
        <h3>
            Total score ({total_score} / {total_possible})
        </h3>
    """.format(total_score=total_score,
               total_possible=total_possible,
               checkOrX=checkOrX
               )
        edxOutput.write(header)

        for q in self.questions:
            if len(q) == 2:
                name = q[1]
            else:
                name = q
            checkOrX = '<span class="incorrect"/>'
            if (self.points[q] >= self.maxes[q]):
                checkOrX = '<span class="correct"/>'
            # messages = '\n<br/>\n'.join(self.messages[q])
            messages = "<pre>%s</pre>" % '\n'.join(self.messages[q])
            output = """
        <div class="test">
          <section>
          <div class="shortform">
            Question {q} ({points}/{max}) {checkOrX}
          </div>
        <div class="longform">
          {messages}
        </div>
        </section>
      </div>
      """.format(q=name,
                 max=self.maxes[q],
                 messages=messages,
                 checkOrX=checkOrX,
                 points=self.points[q]
                 )
            # print "*** output for Question %s " % q[1]
            # print output
            edxOutput.write(output)
        edxOutput.write("</div>")
        edxOutput.close()
        edxOutput = open('edx_grade', 'w')
        edxOutput.write(str(self.points.totalCount()))
        edxOutput.close()

    def fail(self, message, raw=False):
        "Sets sanity check bit to false and outputs a message"
        self.sane = False
        self.assignZeroCredit()
        self.addMessage(message, raw)

    def assignZeroCredit(self):
        self.points[self.currentQuestion] = 0

    def addPoints(self, amt):
        self.points[self.currentQuestion] += amt

    def deductPoints(self, amt):
        self.points[self.currentQuestion] -= amt

    def assignFullCredit(self, message="", raw=False):
        self.points[self.currentQuestion] = self.maxes[self.currentQuestion]
        if message != "":
            self.addMessage(message, raw)

    def addMessage(self, message, raw=False):
        if not raw:
            # We assume raw messages, formatted for HTML, are printed separately
            if self.bool_output_mute:
                util.unmutePrint()
            print('*** ' + message)
            if self.bool_output_mute:
                util.mutePrint()
            message = html.escape(message)
        self.messages[self.currentQuestion].append(message)

    def addMessageToEmail(self, message):
        print("WARNING**** addMessageToEmail is deprecated %s" % message)
        for line in message.split('\n'):
            pass
            # print '%%% ' + line + ' %%%'
            # self.messages[self.currentQuestion].append(line)


class Counter(dict):
    """
    Dict with default 0
    """

    def __getitem__(self, idx):
        try:
            return dict.__getitem__(self, idx)
        except KeyError:
            return 0

    def totalCount(self):
        """
        Returns the sum of counts for all keys.
        """
        return sum(self.values())
