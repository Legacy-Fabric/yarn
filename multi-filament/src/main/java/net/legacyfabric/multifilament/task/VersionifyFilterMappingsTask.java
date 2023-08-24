package net.legacyfabric.multifilament.task;

import java.io.IOException;

import javax.inject.Inject;

import org.gradle.api.file.DirectoryProperty;
import org.gradle.api.file.RegularFileProperty;
import org.gradle.api.tasks.InputDirectory;
import org.gradle.api.tasks.InputFile;

import net.fabricmc.mappingio.MappingReader;
import net.fabricmc.mappingio.MappingWriter;
import net.fabricmc.mappingio.format.MappingFormat;
import net.fabricmc.mappingio.tree.MemoryMappingTree;

import net.legacyfabric.multifilament.mappingsio.FilteringMappingVisitor;

public abstract class VersionifyFilterMappingsTask extends MappingOutputTask {
	@Inject
	public VersionifyFilterMappingsTask() {
		this.getOutputFormat().convention(MappingFormat.ENIGMA);
	}

	@InputFile
	public abstract RegularFileProperty getIntermediaryFile();

	@InputDirectory
	public abstract DirectoryProperty getInputDir();

	void run(MappingWriter var1) throws IOException {
		MemoryMappingTree treeView = new MemoryMappingTree();
		MappingReader.read(this.getIntermediaryFile().get().getAsFile().toPath(), treeView);
		FilteringMappingVisitor mappingVisitor = new FilteringMappingVisitor(var1, treeView);
		MappingReader.read(this.getInputDir().getAsFile().get().toPath(), mappingVisitor);
	}
}
