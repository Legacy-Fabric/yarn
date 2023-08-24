package net.legacyfabric.multifilament.task;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import javax.inject.Inject;

import daomephsta.unpick.constantmappers.datadriven.parser.FieldKey;
import daomephsta.unpick.constantmappers.datadriven.parser.MethodKey;
import daomephsta.unpick.constantmappers.datadriven.parser.v2.UnpickV2Reader;
import daomephsta.unpick.constantmappers.datadriven.parser.v2.UnpickV2Remapper;
import daomephsta.unpick.constantmappers.datadriven.parser.v2.UnpickV2Writer;
import org.gradle.api.tasks.TaskAction;
import org.gradle.workers.WorkAction;
import org.gradle.workers.WorkQueue;

import net.fabricmc.filament.task.RemapUnpickDefinitionsTask;
import net.fabricmc.filament.util.FileUtil;
import net.fabricmc.filament.util.UnpickUtil;
import net.fabricmc.mappingio.MappingReader;
import net.fabricmc.mappingio.tree.MappingTree;
import net.fabricmc.mappingio.tree.MemoryMappingTree;

public abstract class FixedRemapUnpickDefinitionsTask extends RemapUnpickDefinitionsTask {
	public FixedRemapUnpickDefinitionsTask() {
	}

	@TaskAction
	@Override
	public void run() {
		WorkQueue workQueue = this.getWorkerExecutor().noIsolation();
		workQueue.submit(FixedRemapUnpickDefinitionsTask.RemapAction.class, (parameters) -> {
			parameters.getInput().set(this.getInput());
			parameters.getMappings().set(this.getMappings());
			parameters.getSourceNamespace().set(this.getSourceNamespace());
			parameters.getTargetNamespace().set(this.getTargetNamespace());
			parameters.getOutput().set(this.getOutput());
		});
	}

	public abstract static class RemapAction implements WorkAction<RemapUnpickDefinitionsTask.RemapParameters> {
		@Inject
		public RemapAction() {
		}

		public void execute() {
			try {
				File output = this.getParameters().getOutput().getAsFile().get();
				FileUtil.deleteIfExists(output);
				Map<String, String> classMappings = new HashMap<>();
				Map<MethodKey, String> methodMappings = new HashMap<>();
				Map<FieldKey, String> fieldMappings = new HashMap<>();
				MemoryMappingTree mappingTree = new MemoryMappingTree();
				MappingReader.read(this.getParameters().getMappings().getAsFile().get().toPath(), mappingTree);
				int fromM = mappingTree.getNamespaceId(this.getParameters().getSourceNamespace().get());
				int toM = mappingTree.getNamespaceId(this.getParameters().getTargetNamespace().get());
				Iterator var8 = mappingTree.getClasses().iterator();

				while (var8.hasNext()) {
					MappingTree.ClassMapping classDef = (MappingTree.ClassMapping) var8.next();

					String classFrom = classDef.getName(fromM);
					String classTo = classDef.getName(toM);

					if (classFrom == null || classFrom.isEmpty()) {
						if (classTo == null || classTo.isEmpty()) continue;
						classFrom = classTo;
					}

					classMappings.put(classFrom, classTo);
					Iterator var10 = classDef.getMethods().iterator();

					while (var10.hasNext()) {
						MappingTree.MethodMapping methodDef = (MappingTree.MethodMapping) var10.next();
						methodMappings.put(new MethodKey(classFrom, methodDef.getName(fromM), methodDef.getDesc(fromM)), methodDef.getName(toM));
					}

					var10 = classDef.getFields().iterator();

					while (var10.hasNext()) {
						MappingTree.FieldMapping fieldDef = (MappingTree.FieldMapping) var10.next();
						fieldMappings.put(new FieldKey(classFrom, fieldDef.getName(fromM)), fieldDef.getName(toM));
					}
				}

				UnpickV2Reader reader = new UnpickV2Reader(new FileInputStream(this.getParameters().getInput().getAsFile().get()));

				try {
					UnpickV2Writer writer = new UnpickV2Writer();
					reader.accept(new UnpickV2Remapper(classMappings, methodMappings, fieldMappings, writer));
					FileUtil.write(output, UnpickUtil.getLfOutput(writer));
				} catch (Throwable var13) {
					try {
						reader.close();
					} catch (Throwable var12) {
						var13.addSuppressed(var12);
					}

					throw var13;
				}

				reader.close();
			} catch (IOException var14) {
				throw new UncheckedIOException(var14);
			}
		}
	}
}
