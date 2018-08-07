import os
import numpy as np
import sabre

class tracepool(object):
    def __init__(self,workdir = './traces',ratio = 0.1):
        self.work_dir = workdir
        self.trace_list = []
        self.abr_list = [sabre.ThroughputRule,sabre.Bola,sabre.BolaEnh,sabre.DynamicDash,sabre.Dynamic]
        self.sample_list = []
        for p in self.abr_list:
            self.sample_list.append([])
        self.sample()
        for p in os.listdir(self.work_dir):
            for l in os.listdir(self.work_dir + '/' + p):
                if np.random.rand() <= ratio:
                    self.trace_list.append(self.work_dir + '/' + p + '/' + l)

    def sample(self):
        for _trace in self.get_list():
            for _abr, _index in zip(self.abr_list, enumerate(self.abr_list)):
                self.sample_list[_index].append(sabre.execute_model(abr=_abr,trace=_trace))

    def get_list(self):
        return self.trace_list

    def battle(self, agent_result):
        ret = []
        for _index in enumerate(self.abr_list):
            tmp = [0, 0, 0]
            for _trace_index in range(len(self.get_list())):
                for p in agent_result:
                    res = self._battle(p[_trace_index], self.sample_list[_index][_trace_index])
                    tmp[np.argmax(res)] += 1
                    tmp[-1] += 1
            ret.append(tmp[0] * 100.0 / tmp[-1])
        return ret
            
    
    def _battle(self, agent_result):
        total_bitrate0, total_rebuffer0, _ = agent_result[0]
        total_bitrate1, total_rebuffer1, _ = agent_result[1]
        if total_rebuffer0 < total_rebuffer1:
            return [1, -1]
        elif total_rebuffer0 == total_rebuffer1:
            if total_bitrate0 > total_bitrate1:
                return [1, -1]
            elif total_bitrate0 == total_bitrate1:
                return [0, 0]
            else:
                return [-1, 1]
        else:
            return [-1, 1]