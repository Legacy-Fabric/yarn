package net.legacyfabric.multifilament.task;

import net.fabricmc.mappingio.MappingReader;
import net.fabricmc.mappingio.MappingWriter;
import net.fabricmc.mappingio.format.MappingFormat;
import net.fabricmc.mappingio.tree.MappingTree;
import net.fabricmc.mappingio.tree.MemoryMappingTree;

import net.legacyfabric.multifilament.mappingsio.FilteringMappingVisitor;

import org.gradle.api.file.DirectoryProperty;
import org.gradle.api.file.RegularFileProperty;
import org.gradle.api.tasks.InputDirectory;
import org.gradle.api.tasks.InputFile;

import javax.inject.Inject;

import java.io.IOException;
import java.nio.file.FileVisitResult;
import java.nio.file.FileVisitor;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.attribute.BasicFileAttributes;

public abstract class UnifyMappingsTask extends MappingOutputTask {
	@Inject
	public UnifyMappingsTask() {
		this.getOutputFormat().convention(MappingFormat.ENIGMA);
	}

	@InputDirectory
	public abstract DirectoryProperty getUnifiedDir();

	@InputDirectory
	public abstract DirectoryProperty getVersionedDir();

	void run(MappingWriter var1) throws IOException {
		this.getUnifiedDir().getAsFile().get().delete();
		Files.move(this.getOutputDir().getAsFile().get().toPath(), this.getUnifiedDir().getAsFile().get().toPath());
		MemoryMappingTree treeView = new MemoryMappingTree();
		MappingReader.read(this.getUnifiedDir().getAsFile().get().toPath(), treeView);
		MemoryMappingTree mappingTree = new MemoryMappingTree();
		MappingReader.read(this.getVersionedDir().getAsFile().get().toPath(), mappingTree);
		int targetNamespace = treeView.getNamespaceId("intermediary");
		int inputNamespace = mappingTree.getNamespaceId("intermediary");

		for (MappingTree.ClassMapping classMapping : mappingTree.getClasses()) {
			MappingTree.ClassMapping unifiedClass = treeView.getClass(classMapping.getSrcName());

			if (unifiedClass == null) {
				treeView.addClass(classMapping);
			} else {
				unifiedClass.setComment(classMapping.getComment());
				unifiedClass.setDstName(classMapping.getName(inputNamespace), targetNamespace);

				for (MappingTree.FieldMapping fieldMapping : classMapping.getFields()) {
					MappingTree.FieldMapping unifiedField = unifiedClass.getField(fieldMapping.getSrcName(), fieldMapping.getSrcDesc());

					if (unifiedField == null) {
						unifiedClass.addField(fieldMapping);
					} else {
						unifiedField.setComment(fieldMapping.getComment());
						unifiedField.setDstName(fieldMapping.getName(inputNamespace), targetNamespace);
					}
				}

				for (MappingTree.MethodMapping methodMapping : classMapping.getMethods()) {
					MappingTree.MethodMapping unifiedMethod = unifiedClass.getMethod(methodMapping.getSrcName(), methodMapping.getSrcDesc());

					if (unifiedMethod == null) {
						unifiedClass.addMethod(methodMapping);
					} else {
						unifiedMethod.setComment(methodMapping.getComment());
						unifiedMethod.setDstName(methodMapping.getName(inputNamespace), targetNamespace);

						for (MappingTree.MethodArgMapping methodArgMapping : methodMapping.getArgs()) {
							MappingTree.MethodArgMapping unifiedArg = unifiedMethod.getArg(
									methodArgMapping.getArgPosition(), methodArgMapping.getLvIndex(),
									methodArgMapping.getSrcName()
							);

							if (unifiedArg == null) {
								unifiedMethod.addArg(methodArgMapping);
							} else {
								unifiedArg.setComment(methodArgMapping.getComment());
								unifiedArg.setDstName(methodArgMapping.getName(inputNamespace), targetNamespace);
							}
						}

						for (MappingTree.MethodVarMapping methodVarMapping : methodMapping.getVars()) {
							MappingTree.MethodVarMapping unifiedVar = unifiedMethod.getVar(
									methodVarMapping.getLvtRowIndex(), methodVarMapping.getLvIndex(),
									methodVarMapping.getStartOpIdx(), methodVarMapping.getSrcName()
							);

							if (unifiedVar == null) {
								unifiedMethod.addVar(methodVarMapping);
							} else {
								unifiedVar.setComment(methodVarMapping.getComment());
								unifiedVar.setDstName(methodVarMapping.getName(inputNamespace), targetNamespace);
							}
						}
					}
				}
			}
		}

		treeView.accept(var1);

		Files.walkFileTree(this.getUnifiedDir().getAsFile().get().toPath(), new FileVisitor<Path>() {
			@Override
			public FileVisitResult preVisitDirectory(Path dir, BasicFileAttributes attrs) throws IOException {
				return FileVisitResult.CONTINUE;
			}

			@Override
			public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
				file.toFile().delete();
				return FileVisitResult.CONTINUE;
			}

			@Override
			public FileVisitResult visitFileFailed(Path file, IOException exc) throws IOException {
				return FileVisitResult.TERMINATE;
			}

			@Override
			public FileVisitResult postVisitDirectory(Path dir, IOException exc) throws IOException {
				dir.toFile().delete();
				return FileVisitResult.CONTINUE;
			}
		});

		Files.walkFileTree(this.getVersionedDir().getAsFile().get().toPath(), new FileVisitor<Path>() {
			@Override
			public FileVisitResult preVisitDirectory(Path dir, BasicFileAttributes attrs) throws IOException {
				return FileVisitResult.CONTINUE;
			}

			@Override
			public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException {
				file.toFile().delete();
				return FileVisitResult.CONTINUE;
			}

			@Override
			public FileVisitResult visitFileFailed(Path file, IOException exc) throws IOException {
				return FileVisitResult.TERMINATE;
			}

			@Override
			public FileVisitResult postVisitDirectory(Path dir, IOException exc) throws IOException {
				dir.toFile().delete();
				return FileVisitResult.CONTINUE;
			}
		});
	}
}
