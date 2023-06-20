package net.legacyfabric.multifilament.task;

import net.fabricmc.filament.task.base.WithFileInput;
import net.fabricmc.mappingio.MappingReader;
import net.fabricmc.mappingio.MappingWriter;

import net.fabricmc.mappingio.format.MappingFormat;
import net.fabricmc.mappingio.tree.MappingTreeView;

import net.fabricmc.mappingio.tree.MemoryMappingTree;

import net.legacyfabric.multifilament.mappingsio.FilteringMappingVisitor;

import org.gradle.api.file.DirectoryProperty;
import org.gradle.api.file.RegularFileProperty;
import org.gradle.api.tasks.InputDirectory;
import org.gradle.api.tasks.InputFile;

import javax.inject.Inject;

import java.io.IOException;

public abstract class VersionifyMappingsTask extends MappingOutputTask {
	@Inject
	public VersionifyMappingsTask() {
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
