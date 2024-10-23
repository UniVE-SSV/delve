package it.unive.delve;

import it.unive.golisa.frontend.GoFrontEnd;
import it.unive.lisa.LiSA;
import it.unive.lisa.analysis.SimpleAbstractState;
import it.unive.lisa.analysis.heap.pointbased.FieldSensitivePointBasedHeap;
import it.unive.lisa.analysis.nonrelational.value.TypeEnvironment;
import it.unive.lisa.analysis.nonrelational.value.ValueEnvironment;
import it.unive.lisa.analysis.types.InferredTypes;
import it.unive.lisa.interprocedural.ReturnTopPolicy;
import it.unive.lisa.interprocedural.callgraph.RTACallGraph;
import it.unive.lisa.interprocedural.context.ContextBasedAnalysis;
import it.unive.lisa.program.Program;
import it.unive.lisa.conf.LiSAConfiguration;
import it.unive.pylisa.PyFrontend;
import it.unive.pylisa.PyLiSA;
import it.unive.ros.lisa.analysis.constants.ConstantPropagation;

import java.io.IOException;

public class Main {

    public static void main(String[] args) throws IOException {

        LiSAConfiguration conf = new LiSAConfiguration();
        conf.workdir = "output";
        conf.serializeResults = false;
        conf.jsonOutput = false;
        conf.analysisGraphs = LiSAConfiguration.GraphType.HTML_WITH_SUBNODES;
        conf.interproceduralAnalysis = new ContextBasedAnalysis<>();
        conf.callGraph = new RTACallGraph();
        conf.openCallPolicy = ReturnTopPolicy.INSTANCE;
        conf.optimize = false;
        //conf.semanticChecks.add(rosGraphDumper);
        FieldSensitivePointBasedHeap heap = new FieldSensitivePointBasedHeap().bottom();
        TypeEnvironment<InferredTypes> type = new TypeEnvironment<>(new InferredTypes());
        ValueEnvironment<ConstantPropagation> domain = new ValueEnvironment<>(new ConstantPropagation());
        conf.abstractState = new SimpleAbstractState<>(heap, domain, type);
        Program goProgram = GoFrontEnd.processFile("tests/gin/gin.go");

        PyFrontend translator = new PyFrontend("tests/fastapi/microserviceA.py", false);
        Program program = translator.toLiSAProgram();

        LiSA lisa = new LiSA(conf);
        lisa.run(program);
        lisa.run(goProgram);
    }
}